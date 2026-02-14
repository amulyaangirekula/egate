import tkinter as tk

from FaceRecognitionSystem.frontend.main_ui import MainUI
from FaceRecognitionSystem.backend.dbModule import FaceRecognitionDB
from FaceRecognitionSystem.backend.face_recognition import FaceRecognitionSystem
from FaceRecognitionSystem.backend.utils import ensure_directories_exist
from FaceRecognitionSystem.backend.config import DB_CONFIG, DIRECTORIES


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