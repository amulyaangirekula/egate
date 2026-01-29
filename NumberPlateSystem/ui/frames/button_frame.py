"""
Button controls frame with live camera support
"""
import tkinter as tk
from tkinter import ttk, messagebox
from ui.components import HoverButton
from utils.plate_recognition import extract_plate_text
from data.vehicle_database import register_vehicle, verify_vehicle, get_all_vehicles
from config import BTN_BG, TEXT_COLOR

class ButtonFrame:
    def __init__(self, master, app):
        self.app = app
        self.frame = ttk.Frame(master, style='TFrame')
        self.frame.pack(fill=tk.X, pady=15, padx=20)
        
        # Button dimensions
        button_width = 16
        button_height = 2
        button_padx = 5
        
        # Upload button
        self.upload_btn = HoverButton(
            self.frame, 
            text="📷 Upload Image", 
            command=self.handle_upload_image, 
            bg=BTN_BG, 
            fg=TEXT_COLOR,
            font=("Segoe UI", 10, "bold"),
            width=button_width,
            height=button_height,
            borderwidth=0,
            relief=tk.FLAT
        )
        self.upload_btn.pack(side=tk.LEFT, padx=button_padx)
        
        # Register button
        self.register_btn = HoverButton(
            self.frame, 
            text="✅ Register Plate", 
            command=self.handle_register_plate, 
            bg=BTN_BG, 
            fg=TEXT_COLOR,
            font=("Segoe UI", 10, "bold"),
            width=button_width,
            height=button_height,
            borderwidth=0,
            relief=tk.FLAT
        )
        self.register_btn.pack(side=tk.LEFT, padx=button_padx)
        
        # Verify button
        self.verify_btn = HoverButton(
            self.frame, 
            text="🔍 Verify Plate", 
            command=self.handle_verify_plate, 
            bg=BTN_BG, 
            fg=TEXT_COLOR,
            font=("Segoe UI", 10, "bold"),
            width=button_width,
            height=button_height,
            borderwidth=0,
            relief=tk.FLAT
        )
        self.verify_btn.pack(side=tk.LEFT, padx=button_padx)
        
        # Live verify button
        self.live_verify_btn = HoverButton(
            self.frame, 
            text="📹 Live Verify", 
            command=self.handle_live_verify, 
            bg=BTN_BG, 
            fg=TEXT_COLOR,
            font=("Segoe UI", 10, "bold"),
            width=button_width,
            height=button_height,
            borderwidth=0,
            relief=tk.FLAT
        )
        self.live_verify_btn.pack(side=tk.LEFT, padx=button_padx)
        
        # Show database button
        self.show_db_btn = HoverButton(
            self.frame, 
            text="📋 Show Database", 
            command=self.handle_show_database, 
            bg=BTN_BG, 
            fg=TEXT_COLOR,
            font=("Segoe UI", 10, "bold"),
            width=button_width,
            height=button_height,
            borderwidth=0,
            relief=tk.FLAT
        )
        self.show_db_btn.pack(side=tk.LEFT, padx=button_padx)
        
        # Clear button
        self.clear_btn = HoverButton(
            self.frame, 
            text="🗑️ Clear", 
            command=self.handle_clear_all, 
            bg=BTN_BG, 
            fg=TEXT_COLOR,
            font=("Segoe UI", 10, "bold"),
            width=button_width,
            height=button_height,
            borderwidth=0,
            relief=tk.FLAT
        )
        self.clear_btn.pack(side=tk.LEFT, padx=button_padx)
        
        # Track if live verification is active
        self.live_verification_active = False
        self.live_verify_job = None
    
    def handle_upload_image(self):
        """Handle image upload button click"""
        image_frame = self.app.get_image_panel()
        image_frame.upload_image(self.app.update_status)
        self.app.get_results_panel().clear()
    
    def handle_register_plate(self):
        """Handle register plate button click"""
        image_frame = self.app.get_image_panel()
        results_frame = self.app.get_results_panel()
        
        current_image = image_frame.get_current_image()
        if not current_image:
            self.app.update_status("No image loaded")
            return
            
        self.app.update_status("Processing plate recognition...")
        plate = extract_plate_text(current_image, self.app.update_status)
        
        if not plate:
            return
            
        # Register the plate
        result = register_vehicle(plate)
        
        # Display result
        results_frame.clear()
        if result['success']:
            results_frame.display_text(
                f"✅ REGISTRATION SUCCESSFUL\n\n"
                f"Plate: {plate}\n"
                f"Registered at: {result['timestamp']}\n"
                f"Status: Added to database\n"
            )
            self.app.update_status(f"Registered plate: {plate}")
        else:
            results_frame.display_text(
                f"⚠️ ALREADY REGISTERED\n\n"
                f"Plate: {plate}\n"
                f"Status: Already in database\n"
            )
            self.app.update_status(f"Plate already registered: {plate}")
    
    def handle_verify_plate(self):
        """Handle verify plate button click"""
        image_frame = self.app.get_image_panel()
        results_frame = self.app.get_results_panel()
        
        current_image = image_frame.get_current_image()
        if not current_image:
            self.app.update_status("No image loaded")
            return
            
        self.app.update_status("Processing plate recognition...")
        plate = extract_plate_text(current_image, self.app.update_status)
        
        if not plate:
            return
            
        # Verify the plate
        result = verify_vehicle(plate)
        
        # Display result
        results_frame.clear()
        if result['exists']:
            results_frame.display_text(
                f"✅ ACCESS AUTHORIZED\n\n"
                f"Plate: {plate}\n"
                f"Registration: {result['registered_at']}\n"
                f"Status: MATCHED - Access Granted\n"
            )
            self.app.update_status(f"Access granted for plate: {plate}")
        else:
            results_frame.display_text(
                f"❌ ACCESS DENIED\n\n"
                f"Plate: {plate}\n"
                f"Status: NOT FOUND - Access Denied\n"
            )
            self.app.update_status(f"Access denied for plate: {plate}")
    
    def handle_live_verify(self):
        """Handle live verification button click"""
        if self.live_verification_active:
            self.stop_live_verification()
            return
            
        image_frame = self.app.get_image_panel()
        
        # Start the camera if not already running
        if not image_frame.camera_active:
            image_frame.start_camera()
            
        if not image_frame.camera_active:
            messagebox.showerror("Camera Error", "Could not start camera")
            return
            
        # Start live verification
        self.live_verification_active = True
        self.live_verify_btn.config(text="⏹️ Stop Live Verify")
        self.app.update_status("Live verification started")
        
        # Start the verification process
        self.perform_live_verification()
        
    def stop_live_verification(self):
        """Stop the live verification process"""
        self.live_verification_active = False
        self.live_verify_btn.config(text="📹 Live Verify")
        
        if self.live_verify_job:
            self.frame.after_cancel(self.live_verify_job)
            self.live_verify_job = None
            
        self.app.update_status("Live verification stopped")
        
    def perform_live_verification(self):
        """Perform live verification at regular intervals"""
        if not self.live_verification_active:
            return
            
        image_frame = self.app.get_image_panel()
        results_frame = self.app.get_results_panel()
        
        # Capture current frame
        current_image = image_frame.capture_camera_frame()
        
        if current_image:
            self.app.update_status("Processing live camera frame...")
            
            # Process the image with AI
            plate = extract_plate_text(current_image, self.app.update_status)
            
            if plate:
                # Verify the plate
                result = verify_vehicle(plate)
                
                # Display result
                results_frame.clear()
                if result['exists']:
                    results_frame.display_text(
                        f"✅ LIVE ACCESS AUTHORIZED\n\n"
                        f"Plate: {plate}\n"
                        f"Registration: {result['registered_at']}\n"
                        f"Status: MATCHED - Access Granted\n"
                        f"Time: {self.get_current_time()}\n"
                    )
                    self.app.update_status(f"Live access granted for plate: {plate}")
                else:
                    results_frame.display_text(
                        f"❌ LIVE ACCESS DENIED\n\n"
                        f"Plate: {plate}\n"
                        f"Status: NOT FOUND - Access Denied\n"
                        f"Time: {self.get_current_time()}\n"
                    )
                    self.app.update_status(f"Live access denied for plate: {plate}")
        
        # Schedule next verification (every 5 seconds)
        self.live_verify_job = self.frame.after(5000, self.perform_live_verification)
    
    def get_current_time(self):
        """Get formatted current time"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def handle_show_database(self):
        """Handle show database button click"""
        results_frame = self.app.get_results_panel()
        vehicles = get_all_vehicles()
        
        results_frame.clear()
        
        if not vehicles:
            results_frame.display_text("No vehicles registered in database.")
            self.app.update_status("Database is empty")
            return
            
        results_frame.display_text("📋 REGISTERED VEHICLES DATABASE\n\n")
        
        for idx, entry in enumerate(vehicles, 1):
            plate = entry.get('plate', 'Unknown')
            reg_time = entry.get('registered_at', 'Unknown')
            results_frame.append_text(f"{idx}. Plate: {plate}\n   Registered: {reg_time}\n\n")
        
        self.app.update_status(f"Displaying {len(vehicles)} registered vehicles")
    
    def handle_clear_all(self):
        """Handle clear button click"""
        image_frame = self.app.get_image_panel()
        results_frame = self.app.get_results_panel()
        
        # Stop live verification if running
        if self.live_verification_active:
            self.stop_live_verification()
            
        image_frame.clear_image()
        results_frame.clear()
        self.app.update_status("Ready")