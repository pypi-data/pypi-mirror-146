import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

import numpy as np
import pandas as pd
import terality
from numpy import ndarray
from pandas.core.dtypes.generic import ABCSeries
from pandas.io.formats.printing import pprint_thing
from terality._terality.httptransport import HTTP_CONNECTION_POOL_SIZE

from terality._terality.patch_libs.patch_pandas_and_numpy import (
    patch_external_packages,
)

# Previous versions require a pandas version < 1.2.5.
from terality._terality.utils import logger

# TODO To check compatibility of un-released versions, we would compare hashes of patched methods code between
#  future and currently supported versions.

PANDAS_SUPPORTED_VERSIONS = (
    [f"1.2.{i}" for i in range(3, 6)]
    + [f"1.3.{i}" for i in range(6)]
    + [
        f"1.4.{i}" for i in range(10)
    ]  # Support un-released 1.4.x versions at it is very likely to work
)

# Below versions require more numpy API to support and decorator check_figures_equal seems buggy
MATPLOTLIB_SUPPORTED_VERSIONS = (
    [f"3.3.{i}" for i in range(5)]
    + [f"3.4.{i}" for i in range(3)]
    + [
        f"3.5.{i}" for i in range(10)
    ]  # Support un-released 3.5.x versions at it is very likely to work
)


class TeralityPlotAccessor:
    def __init__(self, obj):
        self._obj = obj  # DataFrame/Series

    def hist(self, **kwargs):
        with patch_plot_hist():
            plot = pd.plotting.PlotAccessor(self._obj)
            return plot.hist(**kwargs)


def getdata(a, subok=True):  # pylint: disable=invalid-name
    """
    Early return if the input array is terality NDArray
    Requires a monkey patch as we do not support np.array(copy=False).
    """

    # START PATCH CODE
    if isinstance(a, terality.NDArray):
        return a
    # END PATCH CODE

    try:
        data = a._data
    except AttributeError:
        data = np.array(a, copy=False, subok=subok)
    if not subok:
        return data.view(ndarray)
    return data


def _convert_dx(self, dx, x0, xconv, convert):  # pylint: disable=invalid-name, unused-argument
    """
    Monkey patch replacing "type(xconv) is np.ndarray" by "isinstance(xconv, np.ndarray)" so our instancecheck patching works.
    """

    # START PATCH CODE
    from matplotlib import cbook  # import here to not break client not having matplotlib installed

    assert isinstance(xconv, np.ndarray)
    # END PATCH CODE

    if xconv.size == 0:
        # xconv has already been converted, but maybe empty...
        return convert(dx)

    try:
        # attempt to add the width to x0; this works for
        # datetime+timedelta, for instance

        # only use the first element of x and x0.  This saves
        # having to be sure addition works across the whole
        # vector.  This is particularly an issue if
        # x0 and dx are lists so x0 + dx just concatenates the lists.
        # We can't just cast x0 and dx to numpy arrays because that
        # removes the units from unit packages like `pint` that
        # wrap numpy arrays.
        try:
            x0 = cbook.safe_first_element(x0)
        except (TypeError, IndexError, KeyError):
            pass

        try:
            x = cbook.safe_first_element(xconv)  # pylint: disable=invalid-name
        except (TypeError, IndexError, KeyError):
            x = xconv  # pylint: disable=invalid-name

        delist = False
        if not np.iterable(dx):
            dx = [dx]
            delist = True
        dx = [convert(x0 + ddx) - x for ddx in dx]
        if delist:
            dx = dx[0]
    except (ValueError, TypeError, AttributeError):
        # if the above fails (for any reason) just fallback to what
        # we do by default and convert dx by itself.
        dx = convert(dx)
    return dx


def _compute_plot_data(self):
    """
    Monkey patch modifying the last line changes as terality does not support `apply(axis=0)`.
    """

    data = self.data

    if isinstance(data, ABCSeries):
        label = self.label
        if label is None and data.name is None:
            label = "None"
        data = data.to_frame(name=label)

    # GH16953, _convert is needed as fallback, for ``Series``
    # with ``dtype == object``
    data = data._convert(datetime=True, timedelta=True)
    include_type = [np.number, "datetime", "datetimetz", "timedelta"]

    # GH23719, allow plotting boolean
    if self.include_bool is True:
        include_type.append(np.bool_)

    # GH22799, exclude datetime-like type for boxplot
    exclude_type = None
    if self._kind == "box":
        include_type = [np.number]
        exclude_type = ["timedelta"]

    # GH 18755, include object and category type for scatter plot
    if self._kind == "scatter":
        include_type.extend(["object", "category"])

    numeric_data = data.select_dtypes(include=include_type, exclude=exclude_type)

    try:
        is_empty = numeric_data.columns.empty
    except AttributeError:
        is_empty = len(numeric_data) == 0

    # no non-numeric frames or series allowed
    if is_empty:
        raise TypeError("no numeric data to plot")

    # START PATCH CODE
    # TODO _convert_to_ndarray is used to convert pandas dtypes to numpy dtypes (like nullable ints to floats)
    # self.data = numeric_data.apply(self._convert_to_ndarray)
    self.data = numeric_data
    # END PATCH CODE


def _make_single_plot(self, y, label, i, colors, stacking_id):  # pylint: disable=invalid-name
    """
    Draw a single plot for a 1D input (Series), this function is meant to be called by different threads
    simultaneously.
    """

    ax = self._get_ax(i)  # pylint: disable=invalid-name

    kwds = self.kwds.copy()

    label = pprint_thing(label)
    kwds["label"] = label

    style, kwds = self._apply_style_colors(colors, kwds, i, label)
    if style is not None:
        kwds["style"] = style

    kwds = self._make_plot_keywords(kwds, y)

    # We allow weights to be a multi-dimensional array, e.g. a (10, 2) array,
    # and each sub-array (10,) will be called in each iteration. If users only
    # provide 1D array, we assume the same weights is used for all iterations
    weights = kwds.get("weights", None)
    if weights is not None and np.ndim(weights) != 1:
        kwds["weights"] = weights[:, i]

    artists = self._plot(ax, y, column_num=i, stacking_id=stacking_id, **kwds)
    self._add_legend_handle(artists[0], label, index=i)


def _make_plot(self):
    """
    Monkey patch to parallelize computations over columns.
    The fact that each thread calls ax.hist in a probabilistic way leads to several issues:
    - legends order is probabilistic
    - which bars are in foreground/background is probabilistic
    - stacked=True does not work
    """

    colors = self._get_colors()
    stacking_id = self._get_stacking_id()

    with ThreadPoolExecutor(max_workers=HTTP_CONNECTION_POOL_SIZE) as pool:
        labels_and_values = list(self._iter_data())
        labels = [item[0] for item in labels_and_values]
        values = [item[1] for item in labels_and_values]
        nb_cols = len(labels_and_values)

        out = pool.map(
            _make_single_plot,
            [self] * nb_cols,
            values,
            labels,
            list(range(nb_cols)),
            [colors] * nb_cols,
            [stacking_id] * nb_cols,
            timeout=100,
        )
        _ = list(out)  # triggers the threads ? useless ?


@contextmanager
def patch_plot_hist():  # pylint: disable=too-many-statements
    """
    To be used before calling the pandas method PlotAccessor.plot.hist.
    It enables patching top level pandas/numpy methods and uses some specific monkey patches.
    Note that monkey patches to implement are trickier than for an external lib, because
    we need to patch internal pandas methods (that rely on low level pandas features like block manager).
    """

    try:
        import matplotlib as mpl
    except ImportError as e:
        raise ImportError(
            "The 'matplotlib' package is not installed, can't patch it to make it compatible with Terality."
        ) from e

    if mpl.__version__ not in MATPLOTLIB_SUPPORTED_VERSIONS:
        raise ImportError(
            f"Matplotlib version {mpl.__version__} is installed, but Terality only supports following versions: {MATPLOTLIB_SUPPORTED_VERSIONS}"
        )

    if pd.__version__ not in PANDAS_SUPPORTED_VERSIONS:
        raise ImportError(
            f"Pandas version {pd.__version__} is installed, but plot.hist only supports following versions: {PANDAS_SUPPORTED_VERSIONS}"
        )

    with patch_external_packages():
        # import here to not break client not having matplotlib installed
        from pandas.plotting._matplotlib.core import MPLPlot
        from matplotlib.axes import Axes

        previous_log_level = logger.level
        logger.setLevel(logging.ERROR)

        # `_convert` and `_get_numeric_data` private method are called by pandas `PlotAccessor` code,
        # but these methods are not supported by Terality as they are pandas private API. Thus, we have to patch them.
        # TODO _convert should infer better dtypes like str -> datetimes.
        terality.DataFrame._convert = lambda df, *args, **kwargs: df
        terality.Series._convert = lambda series, *args, **kwargs: series

        # TODO Test pandas behavior on datetimes and handle it
        terality.DataFrame._get_numeric_data = lambda df: df.select_dtypes("number")
        terality.Series._get_numeric_data = lambda series: series

        # Required as we do not support `apply(axis=0)`
        old_compute_plot_data = MPLPlot._compute_plot_data
        MPLPlot._compute_plot_data = _compute_plot_data

        # Required as the module imports the symbol directly, like `from pandas import isna`
        old_isna = pd.plotting._matplotlib.hist.isna
        pd.plotting._matplotlib.hist.isna = pd.isna

        try:
            # Only in pandas 1.4 (maybe 1.3 too)
            old_notna = pd.core.dtypes.missing.notna
            pd.core.dtypes.missing.notna = pd.notna
        except AttributeError:
            pass

        # Required to replace a type check by a isinstance check so our instancecheck patching works
        old_convert_dx = Axes._convert_dx
        Axes._convert_dx = _convert_dx

        # Required as we do not support `copy=False`
        old_getdata = np.ma.getdata
        np.ma.getdata = getdata

        # Required to parallelize hist computation over columns
        # Unnused for now as the probabilistic calls to ax.hist leads to several issues.
        # old_make_plot = HistPlot._make_plot
        # HistPlot._make_plot = _make_plot

        # Required to pass isinstance checks on internal pandas types (like ABCDataFrame)
        terality.Index._typ = "index"
        terality.Series._typ = "series"
        terality.DataFrame._typ = "dataframe"

        try:
            yield
        finally:
            logger.setLevel(previous_log_level)

            MPLPlot._compute_plot_data = old_compute_plot_data
            pd.plotting._matplotlib.hist.isna = old_isna

            try:
                # Only in pandas 1.4 (maybe 1.3 too)
                pd.core.dtypes.missing.notna = old_notna
            except AttributeError:
                pass

            Axes._convert_dx = staticmethod(old_convert_dx)
            np.ma.getdata = old_getdata
            # HistPlot._make_plot = old_make_plot

            terality.DataFrame._convert = None
            terality.DataFrame._get_numeric_data = None

            terality.Index._typ = None
            terality.Series._typ = None
            terality.DataFrame._typ = None
