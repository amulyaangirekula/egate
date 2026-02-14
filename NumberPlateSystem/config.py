import os
from dotenv import load_dotenv

load_dotenv()

# Base directory of NumberPlateSystem
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File paths (ABSOLUTE – IMPORTANT)
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "registered_vehicles.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# API settings
API_KEY = os.getenv("API_KEY")

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAPTURE_INTERVAL = 5

# Color scheme (UI – safe to keep)
DARK_BG = "#1e1e2e"
LIGHT_BG = "#313244"
ACCENT = "#89b4fa"
TEXT_COLOR = "#cdd6f4"
BTN_BG = "#45475a"
SUCCESS_COLOR = "#a6e3a1"
ERROR_COLOR = "#f38ba8"
