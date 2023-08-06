"""
.. include:: ../static/docs/excel/report.md
"""

import pandas as pd
from excel.write import write_dataframe_to_sheet, build_chart


class ExcelReport:
    """
    Generates a multi-sheet Excel workbook with data sheets and charts

    Args:
        filename (str): path to excel file
    """

    def __init__(self, filename, **kwargs):
        self.write_args = []
        self.default_figsize = (15, 10)
        self.filename = filename
        self.contents = kwargs.get("contents", True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.write()

    def _build_contents_df(self):
        """build the sheet containing sheet names and descriptions from self.sheets"""
        data = {"Table Name": [], "Description": []}
        for kwargs in self.write_args:
            data["Table Name"].append(kwargs.get("sheet_name"))
            data["Description"].append(kwargs.pop("description", ""))
        return pd.DataFrame(data, index=list(range(len(data["Table Name"]))))

    def _build_contents_sheet(self, writer):
        """create the sheet of contents sheet"""
        contents_df = self._build_contents_df()

        # setup word wrap
        word_wrap_format = writer.book.add_format()
        word_wrap_format.set_text_wrap()

        # write contents df to writer and get sheet object
        contents_sheet_name = "Contents"
        contents_df.to_excel(writer, sheet_name=contents_sheet_name, index=False)
        contents_sheet = writer.sheets[contents_sheet_name]
        contents_sheet.set_column("A:A", 30)

        # ensure second column wraps
        contents_sheet.set_column("B:B", 120, word_wrap_format)
        for sheet_index, kwargs in enumerate(self.write_args):
            sheet_name = kwargs["sheet_name"]
            # pylint:disable=comparison-with-callable
            if kwargs["method"].__name__ == "build_chart":
                # if it's a chart, link to the underlying data. This isn't ideal, but it is
                # currently not possible to link to a chartsheet in Excel :(
                contents_sheet.write_url(
                    f"A{sheet_index + 2}",
                    f"internal:'{kwargs['data_sheet_name']}'!A1",
                    string=sheet_name,
                    tip="jump to sheet",
                )
            else:
                contents_sheet.write_url(
                    f"A{sheet_index + 2}",
                    f"internal:'{sheet_name}'!A1",
                    string=sheet_name,
                    tip="jump to sheet",
                )

    def add_sheet(
        self,
        df,
        sheet_name,
        description=None,
        column_formats=None,
        **kwargs,
    ):
        """add a sheet to the report

        Args:
            df (pandas.DataFrame): sheet to add
            sheet_name (str): name of sheet for contents
            description (str, optional): description for sheet. Defaults to None.
            column_formats (str | dict, optional): a string containing an excel number format or
                a dictionary of column names and number formats. Defaults to None.
            **sort (bool): whether to apply an auto-filter to the data, enabling
                sort and filter in Excel. Defaults to True.
            **index (bool): whether to write the index. If not provided, index will be kept
                or dropped based on its contents.
                NOTE: Overridden if merge_index is True and the index is a MultiIndex.
            **merge_index (bool): whether to merge multiindex cells for dataframes that have
                more than one index level. Defaults to False.
                NOTE: This will disable sorting as enabling sort requires all cells to be unmerged.
        """
        sheet_dict = {
            "method": write_dataframe_to_sheet,
            "df": df,
            "description": description,
            "sheet_name": sheet_name,
            "column_formats": column_formats,
        }
        sheet_dict.update(kwargs)
        self.write_args.append(sheet_dict)
        return df

    def add_chart(self, df, sheet_name, description=None, **kwargs):
        """add a chart to the report

        Args:
            df (pandas.DataFrame): dataframe containing data to write
            sheet_name (str): name of chartsheet to create
            description (str, optional): description for sheet, displayed in contents.
                Defaults to None.
        """
        chart_dict = {
            "method": build_chart,
            "df": df,
            "description": description,
            "sheet_name": sheet_name,
            "data_sheet_name": kwargs.pop("data_sheet_name", sheet_name + " (data)"),
        }
        chart_dict.update(kwargs)
        self.write_args.append(chart_dict)

    def write(self):
        """write the report to excel

        Args:
            output_excel_file (str): path to output file
        """
        with pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
            self.filename, engine="xlsxwriter"
        ) as writer:

            # table of contents must be written first
            if self.contents is True and len(self.write_args) > 1:
                self._build_contents_sheet(writer)

            for kwargs in self.write_args:
                method = kwargs.get("method")
                method(writer=writer, **kwargs)
