import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from backend.utils import validate_email, validate_name, validate_id
from frontend.theme import LABEL_STYLE, ENTRY_STYLE, BUTTON_STYLE, SECTION_TITLE

class RegisterUI:
    def __init__(self, parent, db_instance, face_recognition_system):
        self.parent = parent
        self.db = db_instance
        self.fr_system = face_recognition_system
        
    def show(self):
        window = tk.Toplevel(self.parent)
        window.title("Register New User")
        window.geometry("900x650")
        window.configure(bg="#f5f7fa")
        
        # Header with gradient
        header = tk.Canvas(window, height=100, bg="#3498db", highlightthickness=0)
        header.pack(fill=tk.X)
        
        # Create gradient effect
        for i in range(100):
            # Gradient from #3498db (blue) to #2c3e50 (dark blue)
            r = int(52 + (44-52) * i/100)
            g = int(152 + (62-152) * i/100)
            b = int(219 + (80-219) * i/100)
            color = f'#{r:02x}{g:02x}{b:02x}'
            header.create_line(0, i, 900, i, fill=color)
        
        # Title overlay on gradient
        header.create_text(450, 50, text="👤 User Registration", 
                          font=("Segoe UI", 24, "bold"), fill="white")
        
        # Main content area
        content_frame = tk.Frame(window, bg="#f5f7fa", padx=40, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - form
        form_frame = tk.Frame(content_frame, bg="white", padx=40, pady=30)
        form_frame.grid(row=0, column=0, sticky="nsew")
        form_frame.configure(highlightbackground="#dcdde1", highlightthickness=1)
        
        tk.Label(form_frame, text="Personal Information", 
                font=("Segoe UI", 16, "bold"), bg="white", fg="#2c3e50").pack(anchor="w", pady=(0, 20))
        
        # Fields container
        fields_frame = tk.Frame(form_frame, bg="white")
        fields_frame.pack(fill=tk.X)
        
        fields = [
            ("Full Name:", "name_entry", "Enter your full name"),
            ("ID Number:", "id_entry", "Enter your ID number"),
            ("Email Address:", "email_entry", "Enter your email address"),
            # ("Access Level:", "access_level", "Select access level")
        ]
        
        entries = {}
        
        for i, (label_text, var_name, placeholder) in enumerate(fields):
            field_container = tk.Frame(fields_frame, bg="white", pady=10)
            field_container.pack(fill=tk.X, pady=5)
            
            tk.Label(field_container, text=label_text, 
                    font=("Segoe UI", 12), bg="white", fg="#34495e").pack(anchor="w")
            
            if var_name == "access_level":
                # Dropdown for access level
                combo = ttk.Combobox(field_container, 
                                    values=["Standard", "Administrator", "Limited", "Temporary"],
                                    font=("Segoe UI", 11))
                combo.set("Standard")
                combo.pack(fill=tk.X, pady=(5, 0))
                entries[var_name] = combo
                
                # Style the combobox
                style = ttk.Style()
                style.configure('TCombobox', padding=5)
            else:
                entry = tk.Entry(field_container, font=("Segoe UI", 11), 
                               bd=1, relief=tk.SOLID, bg="#f8f9fa")
                entry.pack(fill=tk.X, ipady=8, pady=(5, 0))
                entry.insert(0, placeholder)
                entry.config(fg="#95a5a6")
                
                # Add placeholder behavior
                def on_entry_click(event, entry=entry, placeholder=placeholder):
                    if entry.get() == placeholder:
                        entry.delete(0, tk.END)
                        entry.config(fg="#2c3e50")
                
                def on_focusout(event, entry=entry, placeholder=placeholder):
                    if entry.get() == '':
                        entry.insert(0, placeholder)
                        entry.config(fg="#95a5a6")
                
                entry.bind('<FocusIn>', on_entry_click)
                entry.bind('<FocusOut>', on_focusout)
                entries[var_name] = entry
        
        # Right side - face capture preview and instructions
        info_frame = tk.Frame(content_frame, bg="#f5f7fa", padx=20)
        info_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        
        # Camera preview placeholder
        preview_frame = tk.Frame(info_frame, bg="white", width=300, height=200)
        preview_frame.pack(fill=tk.X, pady=10)
        preview_frame.configure(highlightbackground="#dcdde1", highlightthickness=1)
        
        tk.Label(preview_frame, text="📷", font=("Segoe UI", 48), 
                bg="white", fg="#95a5a6").place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(preview_frame, text="Camera Preview", font=("Segoe UI", 12), 
                bg="white", fg="#34495e").place(relx=0.5, rely=0.85, anchor=tk.CENTER)
        
        # Instructions card
        instr_frame = tk.Frame(info_frame, bg="white", padx=20, pady=20)
        instr_frame.pack(fill=tk.X, pady=20)
        instr_frame.configure(highlightbackground="#dcdde1", highlightthickness=1)
        
        tk.Label(instr_frame, text="Registration Instructions", 
                font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
        
        instructions = [
            "1. Fill out all personal information fields",
            "2. Click register to proceed to face capture",
            "3. Look directly at the camera when prompted",
            "4. Multiple images will be taken automatically",
            "5. Stay still until the process completes"
        ]
        
        for instruction in instructions:
            tk.Label(instr_frame, text=instruction, font=("Segoe UI", 11), 
                    bg="white", fg="#34495e", anchor="w", pady=4).pack(fill=tk.X)
        
        # Configure column weights for the content frame
        content_frame.columnconfigure(0, weight=3)
        content_frame.columnconfigure(1, weight=2)
        content_frame.rowconfigure(0, weight=1)
        
        # Buttons frame
        button_frame = tk.Frame(window, bg="#f5f7fa", pady=15)
        button_frame.pack(fill=tk.X)
        
        def register():
            # Clear placeholders before getting values
            for var_name, entry in entries.items():
                if var_name != "access_level" and entry.get() in ["Enter your full name", "Enter your ID number", "Enter your email address"]:
                    entry.delete(0, tk.END)
            
            name = entries["name_entry"].get()
            id_number = entries["id_entry"].get()
            email = entries["email_entry"].get()
            # access_level = entries["access_level"].get()

            if not validate_name(name):
                messagebox.showwarning("Validation", "Invalid name (letters only)")
                return
            if not validate_id(id_number):
                messagebox.showwarning("Validation", "Invalid ID number")
                return
            if not validate_email(email):
                messagebox.showwarning("Validation", "Invalid email address")
                return

            user_id = self.db.add_user(name, id_number, email)
            if not user_id:
                messagebox.showerror("Error", "Database error while registering user")
                return

            messagebox.showinfo("Capture", "Look at the camera to capture your face")
            self.fr_system.capture_training_images(name, user_id)
            messagebox.showinfo("Success", f"Registration complete for {name}. Please train the model.")
            window.destroy()
        
        def cancel():
            window.destroy()
        
        cancel_btn = tk.Button(button_frame, text="Cancel", font=("Segoe UI", 11), 
                              bg="white", fg="#e74c3c", padx=20, pady=8,
                              bd=1, relief=tk.SOLID, command=cancel)
        cancel_btn.pack(side=tk.LEFT, padx=40)
        
        register_btn = tk.Button(button_frame, text="Register User", font=("Segoe UI", 11, "bold"), 
                               bg="#3498db", fg="white", padx=25, pady=8,
                               bd=0, command=register)
        register_btn.pack(side=tk.RIGHT, padx=40)
        
        # Button hover effects
        def on_enter(event, button, bg, fg):
            button.config(background=bg, foreground=fg)
            
        def on_leave(event, button, bg, fg):
            button.config(background=bg, foreground=fg)
            
        cancel_btn.bind("<Enter>", lambda event: on_enter(event, cancel_btn, "#e74c3c", "white"))
        cancel_btn.bind("<Leave>", lambda event: on_leave(event, cancel_btn, "white", "#e74c3c"))
        
        register_btn.bind("<Enter>", lambda event: on_enter(event, register_btn, "#2980b9", "white"))
        register_btn.bind("<Leave>", lambda event: on_leave(event, register_btn, "#3498db", "white"))