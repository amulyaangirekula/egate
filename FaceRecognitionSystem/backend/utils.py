import os
import re
import cv2
import numpy as np
from PIL import Image


import os

def ensure_directories_exist(directories):
    for directory in directories:
        absolute_path = os.path.abspath(directory)  # Ensure it's an absolute path
        if not os.path.exists(absolute_path):
            os.makedirs(absolute_path, exist_ok=True)
            print(f"✅ Directory created: {absolute_path}")
        else:
            print(f"🔹 Directory already exists: {absolute_path}")


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def validate_name(name):
    """Validate that name only contains alphabets and spaces"""
    return bool(name.strip() and name.replace(" ", "").isalpha())

def validate_id(id_number):
    """Validate ID number is not empty"""
    return bool(id_number.strip())

def get_face_recognizer():
    """Return the appropriate face recognizer based on OpenCV version"""
    try:
        return cv2.face.LBPHFaceRecognizer_create()
    except:
        try:
            return cv2.face_LBPHFaceRecognizer.create()
        except:
            raise Exception("OpenCV face recognizer not available")

def get_images_and_labels(path):
    """Get face images and their corresponding IDs from the training directory"""
    # Get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    # Create empty lists for faces and IDs
    faces = []
    ids = []
    
    # Loop through all image paths
    for imagePath in imagePaths:
        try:
            # Skip trainer file
            if imagePath.endswith('Trainner.yml'):
                continue
                
            # Open and convert image to grayscale
            pilImage = Image.open(imagePath).convert('L')
            # Convert PIL image to numpy array
            imageNp = np.array(pilImage, 'uint8')
            
            # Extract ID from filename
            id_num = int(os.path.split(imagePath)[-1].split(".")[1])
            
            # Add face and ID to lists
            faces.append(imageNp)
            ids.append(id_num)
            
        except Exception as e:
            print(f"Error processing image {imagePath}: {e}")
            continue
            
    return faces, ids