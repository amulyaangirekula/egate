"""
Image display panel with camera support
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from config import LIGHT_BG, TEXT_COLOR, ACCENT
from utils.camera import CameraManager

class ImageFrame:
    def __init__(self, master):
        self.frame = ttk.Frame(master, style='TFrame')
        self.frame.pack(pady=10)
        
        # Image container with border
        self.img_border = ttk.Frame(self.frame, style='TFrame', width=420, height=320)
        self.img_border.pack(padx=2, pady=2)
        self.img_border.pack_propagate(False)
        
        # Image label
        self.img_label = tk.Label(self.img_border, bg=LIGHT_BG, text="No Image Selected", fg=TEXT_COLOR)
        self.img_label.pack(fill=tk.BOTH, expand=True)
        
        # Camera controls
        self.cam_controls_frame = ttk.Frame(self.frame, style='TFrame')
        self.cam_controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.cam_status_var = tk.StringVar()
        self.cam_status_var.set("Camera: Off")
        
        self.cam_status_label = ttk.Label(
            self.cam_controls_frame,
            textvariable=self.cam_status_var,
            foreground=TEXT_COLOR
        )
        self.cam_status_label.pack(side=tk.LEFT, padx=5)
        
        self.cam_btn_text = tk.StringVar()
        self.cam_btn_text.set("Start Camera")
        
        self.cam_btn = ttk.Button(
            self.cam_controls_frame,
            textvariable=self.cam_btn_text,
            command=self.toggle_camera
        )
        self.cam_btn.pack(side=tk.RIGHT, padx=5)
        
        self.capture_btn = ttk.Button(
            self.cam_controls_frame,
            text="Capture Frame",
            command=self.capture_camera_frame,
            state=tk.DISABLED
        )
        self.capture_btn.pack(side=tk.RIGHT, padx=5)
        
        # Current image data
        self.current_image = None
        self.camera_active = False
        self.camera = CameraManager()
        self.update_id = None
        
    def upload_image(self, status_callback=None):
        """Upload and display an image"""
        # Stop camera if running
        self.stop_camera()
        
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if not file_path:
            return None
            
        try:
            if status_callback:
                status_callback("Loading image...")
                
            pil_image = Image.open(file_path)
            pil_image.thumbnail((400, 300))
            self.current_image = pil_image
            
            img = ImageTk.PhotoImage(pil_image)
            self.img_label.config(image=img, text="")
            self.img_label.image = img  # Keep a reference
            
            filename = file_path.split("/")[-1]
            if status_callback:
                status_callback(f"Loaded: {filename}")
                
            return pil_image
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            if status_callback:
                status_callback("Error loading image")
            return None
    
    def clear_image(self):
        """Clear the displayed image"""
        self.stop_camera()
        self.current_image = None
        self.img_label.config(image="", text="No Image Selected")
        
    def get_current_image(self):
        """Get the currently loaded image"""
        return self.current_image
        
    def toggle_camera(self):
        """Toggle camera on/off"""
        if self.camera_active:
            self.stop_camera()
        else:
            self.start_camera()
            
    def start_camera(self):
        """Start the camera"""
        try:
            if self.camera.start():
                self.camera_active = True
                self.cam_btn_text.set("Stop Camera")
                self.cam_status_var.set("Camera: Active")
                self.capture_btn.config(state=tk.NORMAL)
                self.update_camera_feed()
        except Exception as e:
            messagebox.showerror("Camera Error", str(e))
            
    def stop_camera(self):
        """Stop the camera"""
        if self.camera_active:
            self.camera.stop()
            self.camera_active = False
            self.cam_btn_text.set("Start Camera")
            self.cam_status_var.set("Camera: Off")
            self.capture_btn.config(state=tk.DISABLED)
            
            # Cancel the update task
            if self.update_id:
                self.img_label.after_cancel(self.update_id)
                self.update_id = None
                
    def update_camera_feed(self):
        """Update the camera feed in the UI"""
        if self.camera_active:
            # Get the current frame
            frame = self.camera.get_tk_image()
            
            if frame:
                # Update the image label
                self.img_label.config(image=frame, text="")
                self.img_label.image = frame
            
            # Schedule the next update
            self.update_id = self.img_label.after(10, self.update_camera_feed)
            
    def capture_camera_frame(self):
        """Capture current camera frame for processing"""
        if not self.camera_active:
            return None
            
        self.current_image = self.camera.capture_frame()
        return self.current_image