# Configuration settings for the application

# Directory configuration
import os

# Get the absolute path of the FaceRecognitionSystem folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory configuration
DIRECTORIES = [
    os.path.join(f'{BASE_DIR}/dataset', "CapturedFaces"),
    os.path.join(f'{BASE_DIR}/dataset', "UnknownFaces")
]

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'amulya@26',
    'database': 'face_recognition'
}


# Face recognition settings
FACE_RECOGNITION = {
    'cascade_file': 'assets\haarcascade_frontalface_default.xml',
    'training_file': 'dataset\CapturedFaces\Trainner.yml',
    'confidence_threshold': 50,
    'poor_match_threshold': 75,
    'samples_per_face': 60
}

# Gate monitoring settings
MONITORING = {
    'default_duration': 20  # Default monitoring duration in seconds
}