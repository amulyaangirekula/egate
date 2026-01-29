"""
Application configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# File paths
DATA_DIR = "NumberPlateSystem/data"
DATA_FILE = os.path.join(DATA_DIR, "registered_vehicles.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# API settings
API_KEY = os.getenv("API_KEY")

# Camera settings
CAMERA_INDEX = 0  # Default camera (usually the built-in webcam)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAPTURE_INTERVAL = 5  # Seconds between live verification attempts

# Color scheme
DARK_BG = "#1e1e2e"
LIGHT_BG = "#313244"
ACCENT = "#89b4fa"
TEXT_COLOR = "#cdd6f4"
BTN_BG = "#45475a"
SUCCESS_COLOR = "#a6e3a1"
ERROR_COLOR = "#f38ba8"
