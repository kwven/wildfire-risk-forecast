from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"

NDVI_RAW_DIR = RAW_DIR / "ndvi_2023"
FIRMS_RAW_DIR = RAW_DIR / "firms"
WEATHER_RAW_DIR = RAW_DIR / "weather"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
MODELS_DIR = OUTPUTS_DIR / "models"
REPORTS_DIR = OUTPUTS_DIR / "reports"

WEST = -17.2
SOUTH = 20.5
EAST = -1.0
NORTH = 36.2
BBOX = f"{WEST},{SOUTH},{EAST},{NORTH}"

YEAR = 2023
GRID_SIZE = 0.25
FIRMS_SOURCE = "VIIRS_SNPP_SP"
FIRMS_DAY_RANGE = 5

GRID_PATH = PROCESSED_DIR / "morocco_ws_grid.geojson"
FIRMS_2023_PATH = FIRMS_RAW_DIR / "firms_viirs_morocco_ws_2023.csv"
NDVI_GRID_2023_PATH = PROCESSED_DIR / "ndvi_grid_2023.csv"
DATASET_2023_PATH = PROCESSED_DIR / "fire_risk_dataset_2023_ndvi_firms.csv"
