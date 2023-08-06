"""
.. include:: ../../static/docs/excel/write/chart.md
"""

from excel.write.sheet import write_dataframe_to_sheet
from excel.common.constants import EXCEL_CHART_TYPES


def build_chart(writer, df, **kwargs):
    """Create a chart in an Excel workbook

    Args:
        writer (pandas.ExcelWriter): writer to write to
        df (pandas.DataFrame): dataframe to generate chart from
        **x (any): a column name to plot on x-axis. If not provided,
            defaults to using index as x-axis
        **y (str | list): a column name, or list of column names, to plot on x-axis. If not
            provided, plots all columns against x.
        **sheet_name (str, optional): the name of the chartsheet to create. Defaults to 'Chart1'.
        **data_sheet_name (str, optional): the name of the sheet to write the data to. Defaults to
            'Sheet1'.
        **title (str, optional): title to give the chart. If not provided, will use the default
            title created by XlsxWriter
            (the series name if one series was passed, no title if multiple series passed).
        **chart_type (str, optional): chart type to create. If none is provided,
            defaults to "line".
            See https://xlsxwriter.readthedocs.io/chart.html for available types
        **chart_subtype (str, optional): chart subtype to create.
            See https://xlsxwriter.readthedocs.io/chart.html for available subtypes
        **options (dict): a dictionary containing options to pass to xlsxwriter's Chart methods.
            Keys must be the name of the method to use as defined
            in https://xlsxwriter.readthedocs.io/chart.html, and values must options
            to pass to those methods as arguments.
    """
    # get keyword arguments
    sheet_name = kwargs.pop("sheet_name", "Chart1")
    data_sheet_name = kwargs.pop("data_sheet_name", "Sheet1")

    # enforce only single index level
    # this may change if I decide to support multiindex charting
    if df.index.nlevels > 1 or df.columns.nlevels > 1:
        raise NotImplementedError(
            "Cannot create a chart from a dataframe with multiple index or column levels"
        )

    chart = _create_chart_object(
        workbook=writer.book,
        chart_type=kwargs.pop("chart_type", "line"),
        chart_subtype=kwargs.pop("chart_subtype", None),
    )

    x_col = kwargs.pop("x", None)
    y_col = kwargs.pop("y", None)

    if x_col is not None and not isinstance(x_col, (int, str, float, bool)):
        raise TypeError("x_col must be the name of a column")

    if y_col is None:
        y_col = [col for col in df.columns if col != x_col]
    if not isinstance(y_col, list):
        y_col = [y_col]

    for y_colname in y_col:
        _add_chart_series(chart, df, data_sheet_name, y_col=y_colname, x_col=x_col)

    # allowing title to be passed directly for convenience.
    # this will be overwritten if name is passed in title_options
    title = kwargs.pop("title", None)
    if title is not None:
        chart.set_title({"name": title})

    options = kwargs.pop("options", None)
    if options is not None:
        _configure_chart_options(chart, options)

    # add chartsheet
    chartsheet = writer.book.add_chartsheet(sheet_name)
    chartsheet.set_chart(chart)

    # ensure the data is written to Excel AFTER the chart is
    # always include index
    write_dataframe_to_sheet(df, writer, sheet_name=data_sheet_name, index=True)


def _configure_chart_options(chart, options):
    """sets chart options from dict"""
    for meth, opts in options.items():
        meth = getattr(chart, meth)
        meth(opts)


def _add_chart_series(chart, df, sheet_name, y_col, x_col=None):
    """add a series to a chart object

    Args:
        chart (xlsxwriter.chart.Chart): chart to add series to
        df (pandas.DataFrame): dataframe containing data to chart
        sheet_name (str): name of sheet containing source data for chart
        y_col (str): name of column to treat as values
        x_col (str, optional): name of column to treat as categories. Defaults to None.
    """

    max_row = df.shape[0]
    x_col = 0 if x_col is None else _get_column_index(df, x_col)
    y_col = _get_column_index(df, y_col)
    chart.add_series(
        {
            "name": [sheet_name, 0, y_col],
            "categories": [sheet_name, 1, x_col, max_row, x_col],
            "values": [sheet_name, 1, y_col, max_row, y_col],
        }
    )


def _create_chart_object(workbook, chart_type, chart_subtype=None):
    """create a chart object with the given parameters, with validation

    Args:
        workbook (xlsxwriter.Workbook): workbook to create chart in
        chart_type (str, optional): chart type to create. If none is provided,
            defaults to "line".
            See https://xlsxwriter.readthedocs.io/chart.html for available types
        chart_subtype (str, optional): chart subtype to create.
            See https://xlsxwriter.readthedocs.io/chart.html for available subtypes

    Raises:
        ValueError: if chart_type is not one of the valid chart types
        ValueError: if chart_subtype is not one of the valid subtypes for chart_type

    Returns:
        xlsxwriter.chart.Chart: Chart object created inside workbook
    """

    # validate arguments
    if chart_type not in EXCEL_CHART_TYPES:
        raise ValueError(
            f"Unknown chart type '{chart_type}'. "
            f"Valid chart types are: {list(EXCEL_CHART_TYPES.keys())}"
        )

    allowed_subtypes = EXCEL_CHART_TYPES[chart_type]
    if chart_subtype is not None and chart_subtype not in allowed_subtypes:
        raise ValueError(
            f"Unknown {chart_type} subtype '{chart_subtype}'"
            f"Valid {chart_type} subtypes are: {allowed_subtypes}"
        )

    chart_opts = {"type": chart_type}
    if chart_subtype is not None:
        chart_opts["subtype"] = chart_subtype

    return workbook.add_chart(chart_opts)


def _get_column_index(df, col_name):
    """get the index (from zero) of a column name in a dataframe

    Args:
        df (pandas.DataFrame): dataframe containing columns to search
        col_name (str): name of column to get index for

    Raises:
        ValueError: if the column provided is not in df

    Returns:
        int: column index
    """

    cols_as_list = df.columns.tolist()
    try:
        return cols_as_list.index(col_name) + df.index.nlevels
    except ValueError as exc:
        raise ValueError(
            f"Column '{col_name}' not found in columns. Columns were: '{cols_as_list}'"
        ) from exc
