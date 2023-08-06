"""pandas integration"""

from io import BytesIO
from pathlib import Path
import pandas as pd
from excel.report import ExcelReport
from excel.write.sheet import write_dataframe_to_sheet
from excel.write.chart import build_chart


@pd.api.extensions.register_dataframe_accessor("excel")
class ExcelAccessor:
    """integrate pandas-excel into Dataframes"""

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def to_sheet(self, path_or_report, *args, **kwargs):
        """
        write to a sheet of an Excel workbook, either by adding to an existing ExcelReport
        or by writing directly to a file

        Args:
            path_or_report (str | pathlib.Path | excel.ExcelReport): path or report to write to
        *args, **kwargs: arguments passed to write_dataframe_to_sheet
        """

        self._write(path_or_report, "sheet", *args, **kwargs)

    def to_chart(self, path_or_report, *args, **kwargs):
        """
        write to a chartsheet of an Excel workbook, either by adding to an existing ExcelReport
        or by writing directly to a file

        Args:
            path_or_report (str | pathlib.Path | io.BytesIO | excel.ExcelReport):
                path or report to write to
            *args, **kwargs: arguments passed to build_chart
        """

        self._write(path_or_report, "chart", *args, **kwargs)

    def _write(self, path_or_report, sheet_or_chart, *args, **kwargs):
        assert sheet_or_chart in ["sheet", "chart"]

        if isinstance(path_or_report, (str, Path, BytesIO)):
            with pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
                path_or_report, engine="xlsxwriter"
            ) as writer:
                if sheet_or_chart == "sheet":
                    write_dataframe_to_sheet(self._obj, writer, *args, **kwargs)
                else:
                    build_chart(writer, self._obj, **kwargs)

        elif isinstance(path_or_report, ExcelReport):
            if sheet_or_chart == "sheet":
                path_or_report.add_sheet(self._obj, *args, **kwargs)
            else:
                path_or_report.add_chart(self._obj, *args, **kwargs)

        else:
            raise TypeError(
                "path_or_report must be str, pathlib.Path or excel.ExcelReport, "
                f"not {type(path_or_report)}"
            )
