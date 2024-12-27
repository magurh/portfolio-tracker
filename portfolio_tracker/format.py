import pandas as pd

# Formatting columns for Portfolio Manager
COLUMNS_TO_FORMAT = [
    "Realized gains",
    "Rate of return (%)",
    "Initial investment",
    "Total value sold",
]
DATE_COLUMN = "Date last sell"


# Formatting helper for Portfolio Manager
def format_dataframe(
    _dataframe: pd.DataFrame,
    cols_to_format: list = COLUMNS_TO_FORMAT,
    decimals: int = 2,
    date_column: str = DATE_COLUMN,
) -> pd.DataFrame:
    """Format numerical and date columns."""
    # Format numerical column
    for column in cols_to_format:
        _dataframe[column] = _dataframe[column].apply(lambda x: f"{x:.{decimals}f}")

    # Format data column
    if date_column:
        _dataframe[date_column] = _dataframe[date_column].dt.strftime("%d-%m-%Y")
    return _dataframe
