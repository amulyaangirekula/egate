# Configuration settings for the application

import os

# -------------------------------------------------
# PATH CONFIGURATION
# -------------------------------------------------

# Absolute path of backend folder
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute path of FaceRecognitionSystem folder
PROJECT_DIR = os.path.abspath(os.path.join(BACKEND_DIR, ".."))

# -------------------------------------------------
# DIRECTORY CONFIGURATION
# -------------------------------------------------

DIRECTORIES = [
    os.path.join(BACKEND_DIR, "dataset", "CapturedFaces"),
    os.path.join(BACKEND_DIR, "dataset", "UnknownFaces")
]

# -------------------------------------------------
# DATABASE CONFIGURATION
# -------------------------------------------------

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'amulya@26',
    'database': 'face_recognition'
}

# -------------------------------------------------
# FACE RECOGNITION SETTINGS
# -------------------------------------------------

FACE_RECOGNITION = {
    # assets folder is OUTSIDE backend
    'cascade_file': os.path.join(
        PROJECT_DIR,
        'assets',
        'haarcascade_frontalface_default.xml'
    ),

    # trainer file is inside backend/dataset
    'training_file': os.path.join(
        BACKEND_DIR,
        'dataset',
        'CapturedFaces',
        'Trainner.yml'
    ),

    'confidence_threshold': 50,
    'poor_match_threshold': 75,
    'samples_per_face': 60
}

# -------------------------------------------------
# GATE MONITORING SETTINGS
# -------------------------------------------------

MONITORING = {
    'default_duration': 20  # seconds
}
