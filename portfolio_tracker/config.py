from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path

from portfolio_tracker.utils import get_data_folder_path


@dataclass(frozen=True, kw_only=True)
class Config:
    data_path: Path
    type1_path: Path
    type2_path: Path
    type3_path: Path


def load_env_var(var_name: str) -> str:
    """Loads and validates environment variables."""
    env_var = os.getenv(var_name, default="")
    if not env_var:
        msg = f"'{var_name}' not found in env"
        raise ValueError(msg)
    return env_var


# Set paths
PRIVATE_PATH = load_env_var("PRIVATE_PATH")
if PRIVATE_PATH:
    DATA_PATH = Path(get_data_folder_path(data_type="private"))
else:
    DATA_PATH = Path(get_data_folder_path())

config = Config(
    data_path=DATA_PATH,
    type1_path=DATA_PATH / "type1.csv",
    type2_path=DATA_PATH / "type2.csv",
    type3_path=DATA_PATH / "type3.csv",
)

# Formatting constants
COLUMNS_TO_FORMAT = [
    "Realized gains",
    "Rate of return (%)",
    "Initial investment",
    "Total value sold",
]
DATE_COLUMN = "Date last sell"


# Formatting helper
def format_dataframe(df):
    """Format numerical and date columns."""
    for column in COLUMNS_TO_FORMAT:
        df[column] = df[column].apply(lambda x: f"{x:.2f}")
    df[DATE_COLUMN] = df[DATE_COLUMN].dt.strftime("%d-%m-%Y")
    return df
