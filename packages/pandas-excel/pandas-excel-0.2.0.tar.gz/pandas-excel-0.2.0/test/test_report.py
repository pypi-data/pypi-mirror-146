"""tests for report module"""

from io import BytesIO
import openpyxl
import pandas as pd
import pytest
from excel import ExcelReport, formats

valid_sheet_name = (
    lambda sheet_name: sheet_name if len(sheet_name) <= 31 else sheet_name[0:31]
)


@pytest.mark.parametrize(
    ("fixture_name", "kwargs"),
    [
        ("test_datetime_index_single_column", None),
        (
            "test_categorical_index_single_column",
            {"description": "sheet description goes here"},
        ),
        (
            "test_categorical_index_multi_column",
            {"column_formats": {"2015": formats.PERCENTAGE}},
        ),
    ],
)
def test_add_sheet(fixture_name, kwargs, request):
    """test add_sheet method of ExcelReport class"""
    kwargs = kwargs if kwargs is not None else {}
    out = BytesIO()
    report = ExcelReport(out)
    report.add_sheet(
        request.getfixturevalue(fixture_name), sheet_name=fixture_name, **kwargs
    )
    for write_args in report.write_args:
        if write_args["sheet_name"] == fixture_name:
            assert isinstance(write_args["df"], pd.DataFrame)
            assert write_args["description"] == kwargs.get("description")
            assert write_args["column_formats"] == kwargs.get("column_formats")
            return
    pytest.fail(f"Sheet '{fixture_name}' not found")


@pytest.mark.parametrize(
    ("fixture_name", "kwargs"),
    [
        ("test_datetime_index_single_column", None),
        (
            "test_categorical_index_single_column",
            {"description": "sheet description goes here"},
        ),
    ],
)
def test_add_chart(fixture_name, kwargs, request):
    """test add_sheet method of ExcelReport class"""
    kwargs = kwargs if kwargs is not None else {}
    out = BytesIO()
    report = ExcelReport(out)
    report.add_chart(
        request.getfixturevalue(fixture_name), sheet_name=fixture_name, **kwargs
    )
    for write_args in report.write_args:
        if write_args["sheet_name"] == fixture_name:
            assert isinstance(write_args["df"], pd.DataFrame)
            assert write_args["description"] == kwargs.get("description")
            return
    pytest.fail(f"Sheet '{fixture_name}' not found")


def test_write_multisheet(test_datetime_index_single_column):
    """test write method of ExcelReport class

    Args:
        fixture_names (str | list): fixture name or list of fixture names to write to report
        add_method (str, one of {"add_sheet", "add_chart"}): name of method to pass kwargs to
        kwargs (dict): keyword arguments passed to add_sheet or add_chart
    """

    out = BytesIO()
    with ExcelReport(out) as report:
        report.add_sheet(
            test_datetime_index_single_column, "data only", description="Data Only"
        )
        report.add_chart(
            test_datetime_index_single_column, "chart", description="chart"
        )
    workbook = openpyxl.open(out)
    assert len(workbook.worksheets) == 3
    assert len(workbook.chartsheets) == 1
