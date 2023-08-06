"""tests for _pandas_integration module"""

from io import BytesIO
import openpyxl
import pandas as pd
import pytest
import excel

out = BytesIO()


def test_integrated_successfully():
    """test integration worked"""

    df = pd.DataFrame()
    assert hasattr(df, "excel")


def test_to_sheet(test_datetime_index_single_column):
    """test to_sheet method of ExcelAccessor"""

    test_datetime_index_single_column.excel.to_sheet(out)
    workbook = openpyxl.open(out)
    assert len(workbook.worksheets) == 1


def test_to_chart(test_datetime_index_single_column):
    """test to_chart method of ExcelAccessor"""
    test_datetime_index_single_column.excel.to_chart(out)
    workbook = openpyxl.open(out)
    assert len(workbook.worksheets) == 1


@pytest.mark.parametrize(
    ("path_or_report", "sheet_or_chart", "exception"),
    [
        (BytesIO(), "sheet", None),
        (BytesIO(), "chart", None),
        (excel.ExcelReport(out), "sheet", None),
        (excel.ExcelReport(out), "chart", None),
        (None, "sheet", TypeError),
    ],
)
def test__write(
    test_datetime_index_single_column, path_or_report, sheet_or_chart, exception
):
    def do_test():
        if sheet_or_chart == "sheet":
            test_datetime_index_single_column.excel.to_sheet(
                path_or_report, sheet_or_chart
            )
        else:
            test_datetime_index_single_column.excel.to_chart(
                path_or_report, sheet_or_chart
            )

    if exception is None:
        do_test()
    else:
        with pytest.raises(exception):
            do_test()
