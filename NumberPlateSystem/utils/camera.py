"""
Camera handling utilities for live license plate recognition
"""
import cv2
import threading
import time
from PIL import Image, ImageTk

class CameraManager:
    def __init__(self, video_source=0):
        """
        Initialize the camera manager
        
        Args:
            video_source: Camera index (default is 0 for built-in webcam)
        """
        self.video_source = video_source
        self.camera = None
        self.is_running = False
        self.frame = None
        self.processed_frame = None
        self.frame_count = 0
        self.last_frame_time = 0
        self.fps = 0
        
    def start(self):
        """Start camera capture"""
        if self.is_running:
            return
            
        # Open video capture
        self.camera = cv2.VideoCapture(self.video_source)
        
        if not self.camera.isOpened():
            raise ValueError("Could not open camera")
            
        # Set camera properties
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.is_running = True
        
        # Start capture thread
        self.thread = threading.Thread(target=self._capture_loop)
        self.thread.daemon = True
        self.thread.start()
        
        return True
        
    def stop(self):
        """Stop camera capture"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        
        if self.camera:
            self.camera.release()
            self.camera = None
            
    def _capture_loop(self):
        """Background thread for continuous frame capture"""
        while self.is_running:
            ret, frame = self.camera.read()
            
            if ret:
                # Calculate FPS
                current_time = time.time()
                if self.last_frame_time:
                    time_diff = current_time - self.last_frame_time
                    if time_diff > 0:
                        self.fps = 1.0 / time_diff
                self.last_frame_time = current_time
                
                # Convert the frame to RGB (from BGR)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Update the current frame
                self.frame = frame_rgb
                self.frame_count += 1
            
            # Sleep to control frame rate
            time.sleep(0.01)
    
    def get_frame(self):
        """
        Get the current frame
        
        Returns:
            Current frame as numpy array (RGB)
        """
        return self.frame
        
    def get_pil_image(self):
        """
        Get the current frame as a PIL Image
        
        Returns:
            PIL Image object or None if no frame available
        """
        if self.frame is not None:
            return Image.fromarray(self.frame)
        return None
    
    def get_tk_image(self, max_width=400, max_height=300):
        """
        Get the current frame as a Tkinter PhotoImage
        
        Args:
            max_width: Maximum width for resizing
            max_height: Maximum height for resizing
            
        Returns:
            Tkinter PhotoImage or None if no frame available
        """
        pil_image = self.get_pil_image()
        if pil_image:
            # Resize the image to fit display area
            width, height = pil_image.size
            
            # Calculate the ratio of the width and height to the max dimensions
            width_ratio = max_width / width
            height_ratio = max_height / height
            
            # Use the smaller ratio to ensure the image fits within bounds
            ratio = min(width_ratio, height_ratio)
            
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
            
            return ImageTk.PhotoImage(pil_image)
        return None
    
    def capture_frame(self):
        """
        Capture the current frame for processing
        
        Returns:
            PIL Image of the captured frame or None if no frame available
        """
        if self.frame is not None:
            return Image.fromarray(self.frame)
        return None