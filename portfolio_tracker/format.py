import pandas as pd


# Formatting helper for Portfolio Manager
def format_dataframe(
    _dataframe: pd.DataFrame,
    cols_to_format: list = "",
    decimals: int = 2,
    date_column: str = "",
) -> pd.DataFrame:
    """Format numerical and date columns."""
    # Format numerical column
    for column in cols_to_format:
        _dataframe[column] = _dataframe[column].apply(lambda x: f"{x:.{decimals}f}")

    # Format data column
    if date_column:
        _dataframe[date_column] = _dataframe[date_column].dt.strftime("%d-%m-%Y")
    return _dataframe
