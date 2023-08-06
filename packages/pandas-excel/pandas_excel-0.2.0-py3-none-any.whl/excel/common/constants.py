"""shared constants"""

ILLEGAL_SHEET_NAME_CHARACTERS = ['"', "/", "*", "?", ":", "[", "]"]

EXCEL_CHART_TYPES = {
    "area": ["stacked", "percent_stacked"],
    "bar": ["stacked", "percent_stacked"],
    "column": ["stacked", "percent_stacked"],
    "scatter": ["straight_with_markers", "straight", "smooth_with_markers", "smooth"],
    "line": ["stacked", "percent_stacked"],
    "radar": ["with_markers", "filled"],
}
