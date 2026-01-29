import tkinter as tk

from backend.dbModule import FaceRecognitionDB
from backend.face_recognition import FaceRecognitionSystem
from frontend.ui_components_tkinter import MainUI
from backend.utils import ensure_directories_exist
from backend.config import DB_CONFIG, DIRECTORIES

def main():
    # Ensure directories exist
    ensure_directories_exist(DIRECTORIES)
    
    # Initialize database
    try:
        db = FaceRecognitionDB(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
    except Exception as e:
        print(f"Database initialization error: {e}")
        return
    
    # Initialize face recognition system
    face_recognition_system = FaceRecognitionSystem(db)
    
    # Create main window
    window = tk.Tk()
    
    # Setup UI
    app = MainUI(window, db, face_recognition_system)
    
    # Run the application
    window.mainloop()

if __name__ == "__main__":
    main()