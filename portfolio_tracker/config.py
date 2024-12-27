import os

from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path

from portfolio_tracker.utils import get_data_folder_path

# Load the .env file
load_dotenv()


@dataclass(frozen=True)
class VisualizerColors:
    bg_color: str
    txt_color: str
    green_color: str
    red_color: str
    blue_color: str


@dataclass(frozen=True, kw_only=True)
class Config:
    data_path: Path
    type1_path: Path
    type2_path: Path
    type3_path: Path
    colors: VisualizerColors


def load_env_var(var_name: str) -> str:
    """Loads and validates environment variables."""
    env_var = os.getenv(var_name, default="")
    if not env_var:
        msg = f"'{var_name}' not found in env"
        raise ValueError(msg)
    return env_var


# Set paths
PRIVATE_PATH = load_env_var("PRIVATE_PATH")
DATA_PATH = Path(get_data_folder_path(data_type=PRIVATE_PATH))

config = Config(
    data_path=DATA_PATH,
    type1_path=DATA_PATH / "type1.csv",
    type2_path=DATA_PATH / "type2.csv",
    type3_path=DATA_PATH / "type3.csv",
    colors=VisualizerColors(
        bg_color="#1e1e1e",
        txt_color="white",
        green_color="#00563E",
        red_color="#540202",
        blue_color="lightseagreen",
    ),
)
