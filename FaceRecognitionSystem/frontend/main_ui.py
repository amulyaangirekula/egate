import tkinter as tk
from tkinter import messagebox, ttk
from frontend.register_ui import RegisterUI
from frontend.history_ui import HistoryUI
from frontend.theme import TITLE_FONT, BUTTON_STYLE
from PIL import Image, ImageTk

class MainUI:
    def __init__(self, window, db_instance, face_recognition_system):
        self.window = window
        self.db = db_instance
        self.fr_system = face_recognition_system
        self.setup_homepage()

    def setup_homepage(self):
        self.window.title("Gate Access Control System")
        self.window.geometry("1200x700")
        self.window.configure(bg="#f5f7fa")
        
        # Modern gradient header
        header_frame = tk.Frame(self.window, bg="#3498db", height=120)
        header_frame.pack(fill=tk.X)
        
        # Create canvas for gradient effect
        canvas = tk.Canvas(header_frame, height=120, bg="#3498db", highlightthickness=0)
        canvas.pack(fill=tk.X)
        
        # Create gradient effect
        for i in range(120):
            # Gradient from #3498db (blue) to #2c3e50 (dark blue)
            r = int(52 + (44-52) * i/120)
            g = int(152 + (62-152) * i/120)
            b = int(219 + (80-219) * i/120)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, 1200, i, fill=color)
        
        # Add logo
        logo_img = Image.open("logo.png")  # Make sure this file exists in your project directory
        logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)
        self.logo = ImageTk.PhotoImage(logo_img)
        canvas.create_image(60, 60, image=self.logo)  # Adjust position as needed

        # Title overlay on gradient
        canvas.create_text(600, 25, text="Chaitanya Bharathi Institute of Technology (CBIT)", 
                        font=("Segoe UI", 16, "bold"), fill="#ecf0f1")

        canvas.create_text(600, 55, text="🚪 AI-Based E-Gate Management System", 
                        font=("Segoe UI", 28, "bold"), fill="white")

        canvas.create_text(600, 90, text="Face Recognition System", 
                        font=("Segoe UI", 14, "italic"), fill="#ecf0f1")

        # Main content area with nice padding
        content_frame = tk.Frame(self.window, bg="#f5f7fa")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Left side - information panel with rounded corners effect
        info_frame = tk.Frame(content_frame, bg="white", bd=0)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Add shadow effect with slightly rounded appearance
        info_frame.configure(highlightbackground="#dcdde1", highlightthickness=1)
        
        # Info panel content with improved spacing
        system_info = tk.Label(info_frame, text="Welcome", font=("Segoe UI", 18, "bold"), 
                              bg="white", fg="#2c3e50", pady=15)
        system_info.pack(fill=tk.X, padx=20)
        
        # Status indicators with improved styling
        status_frame = tk.Frame(info_frame, bg="white", pady=10)
        status_frame.pack(fill=tk.X, padx=20)

        # Section title
        tk.Label(status_frame, text="Project Information", font=("Segoe UI", 14, "bold"), 
                bg="white", fg="#2c3e50").pack(anchor="w", pady=(0, 10))

        # Create status indicators with card-like appearance and different colors
        statuses = [
            ("Project ID", "01", "#3498db"),  # Blue
            ("Team", "Akshitha (160122733001), Amulya (160122733003)", "#2ecc71"),  # Green
            ("Institute", "CBIT, Hyderabad", "#9b59b6")  # Purple
        ]

        for i, (label, value, color) in enumerate(statuses):
            # Create a card-like container for each status
            card = tk.Frame(status_frame, bg="white", bd=0, highlightbackground=color, 
                        highlightthickness=1, padx=2, pady=2)
            card.pack(fill=tk.X, pady=8, ipady=8)
            
            # Add a color accent bar on the left
            accent = tk.Frame(card, bg=color, width=5)
            accent.pack(side=tk.LEFT, fill=tk.Y)
            
            # Text content container
            content = tk.Frame(card, bg="white")
            content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            
            # Label with smaller font to emphasize the value
            status_label = tk.Label(content, text=f"{label}:", 
                                font=("Segoe UI", 11), bg="white", fg="#7f8c8d")
            status_label.pack(anchor="w")
            
            # Value with larger bold font and color
            status_value = tk.Label(content, text=value, 
                                font=("Segoe UI", 13, "bold"), bg="white", fg=color)
            status_value.pack(anchor="w", pady=(2, 0))
            
            # Add subtle hover effect
            def on_enter(e, card=card, color=color):
                card.config(highlightbackground=color, highlightthickness=2)
                
            def on_leave(e, card=card, color=color):
                card.config(highlightbackground=color, highlightthickness=1)
                
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
        
        # # Dynamic system stats with gauge-like visualization
        # stats_frame = tk.Frame(info_frame, bg="white", pady=15)
        # stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # # Add a live system stats section with visual indicators
        # tk.Label(stats_frame, text="📊 System Status", font=("Segoe UI", 14, "bold"), 
        #         bg="white", fg="#2c3e50").pack(anchor="w", pady=(0, 10))
        
        # # Status bars for system metrics
        # metrics = [
        #     ("Model Accuracy", 94, "#2ecc71"),
        #     ("Database Performance", 87, "#3498db"),
        #     ("System Load", 42, "#f39c12")
        # ]
        
        # for name, value, color in metrics:
        #     metric_frame = tk.Frame(stats_frame, bg="white")
        #     metric_frame.pack(fill=tk.X, pady=3)
            
        #     # Label and value
        #     label_frame = tk.Frame(metric_frame, bg="white")
        #     label_frame.pack(fill=tk.X)
            
        #     tk.Label(label_frame, text=name, font=("Segoe UI", 10), 
        #             bg="white", fg="#34495e").pack(side=tk.LEFT)
        #     tk.Label(label_frame, text=f"{value}%", font=("Segoe UI", 10, "bold"), 
        #             bg="white", fg=color).pack(side=tk.RIGHT)
            
        #     # Create style for this specific progress bar
        #     progress_style = f"{name.replace(' ', '')}.Horizontal.TProgressbar"
        #     style = ttk.Style()
        #     style.configure(progress_style, background=color, troughcolor="#ecf0f1")
            
        #     # Progress bar
        #     progress = ttk.Progressbar(metric_frame, value=value, maximum=100, 
        #                               style=progress_style)
        #     progress.pack(fill=tk.X, pady=2)

        # SCROLLABLE KEY FEATURES SECTION
        features_section = tk.Frame(info_frame, bg="white", pady=15)
        features_section.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Title for features section
        tk.Label(features_section, text="✨ Key Features", font=("Segoe UI", 14, "bold"), 
                bg="white", fg="#2c3e50").pack(anchor="w", pady=(0, 10))
        
        # Create scrollable container
        # First, create a canvas and scrollbar
        features_canvas = tk.Canvas(features_section, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(features_section, orient="vertical", command=features_canvas.yview)
        
        # Configure the scrollable frame
        features_frame = tk.Frame(features_canvas, bg="white")
        features_frame.bind("<Configure>", 
                           lambda e: features_canvas.configure(scrollregion=features_canvas.bbox("all")))
        
        # Create a window in the canvas for the features frame
        canvas_frame = features_canvas.create_window((0, 0), window=features_frame, anchor="nw")
        
        # Configure the canvas to expand with the window and update the scroll region
        def configure_canvas(event):
            features_canvas.itemconfig(canvas_frame, width=event.width)
        features_canvas.bind("<Configure>", configure_canvas)
        
        # Add the canvas and scrollbar to the features section
        features_canvas.configure(yscrollcommand=scrollbar.set)
        features_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure grid in the features frame
        features_frame.columnconfigure(0, weight=1)
        features_frame.columnconfigure(1, weight=1)
        
        # Key features with icons and colors
        features = [
            ("📷", "Capture Faces", "Capture training images with face detection.", "#3498db"),
            ("🧠", "Train Model", "Trains LBPH model using registered user faces.", "#9b59b6"),
            ("🎥", "Monitor Gate", "Real-time face matching to authorize entry.", "#2ecc71"),
            ("🚫", "Intruder Detection", "Logs and stores faces of unknown visitors.", "#e74c3c"),
            ("📊", "Access Logging", "Records every entry attempt with timestamp.", "#f39c12"),
            ("💾", "Offline Storage", "Stores data and access logs securely offline.", "#1abc9c"),
            ("🔁", "Live Feedback", "Displays detection result with name/status.", "#8e44ad"),
            ("📂", "Auto Save Unknown", "Saves unauthorized faces for review/training.", "#d35400"),
        ]
        
        # Create card for each feature with enhanced styling
        for i, (icon, title, desc, color) in enumerate(features):
            row, col = divmod(i, 2)
            
            # Create feature card with subtle gradient effect
            card = tk.Frame(features_frame, bg="white", bd=0, highlightbackground=color, 
                           highlightthickness=2, padx=5, pady=5)
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Card content frame for better padding
            content = tk.Frame(card, bg="white")
            content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Add icon with larger size
            icon_label = tk.Label(content, text=icon, font=("Segoe UI", 28), bg="white", fg=color)
            icon_label.pack(anchor="w", padx=5, pady=(5, 0))
            
            # Add title with improved font
            title_label = tk.Label(content, text=title, font=("Segoe UI", 12, "bold"), 
                                  bg="white", fg="#2c3e50")
            title_label.pack(anchor="w", padx=5)
            
            # Add description with better spacing
            desc_label = tk.Label(content, text=desc, font=("Segoe UI", 10), 
                                 bg="white", fg="#7f8c8d", wraplength=160, justify=tk.LEFT)
            desc_label.pack(anchor="w", padx=5, pady=(2, 5))
            
            # Add hover effect for cards
            def on_enter(e, card=card, color=color):
                card.config(highlightbackground=self.brighten_color(color))
                
            def on_leave(e, card=card, color=color):
                card.config(highlightbackground=color)
                
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
        
        # Right side - action buttons with improved styling
        button_frame = tk.Frame(content_frame, bg="#f5f7fa", width=300)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        
        # Add title to button section
        tk.Label(button_frame, text="Actions", font=("Segoe UI", 16, "bold"), 
                bg="#f5f7fa", fg="#2c3e50").pack(anchor="w", pady=(0, 15))
        
        # Function buttons with enhanced styling
        actions = [
            ("👤 Register User", self.open_register_ui, "#3498db"),
            ("🧠 Train System", self.train_system, "#9b59b6"),
            ("🎥 Monitor Gate", self.monitor_gate, "#2ecc71"),
            ("📂 Access History", self.view_access_history, "#e67e22"),
            ("❌ Quit", self.window.quit, "#e74c3c")
        ]
        
        for text, command, color in actions:
            # Create button with hover effect and improved styling
            btn_frame = tk.Frame(button_frame, bg="#f5f7fa", cursor="hand2")
            btn_frame.pack(fill=tk.X, pady=8)
            
            btn = tk.Button(btn_frame, text=text, command=command, 
                           font=("Segoe UI", 13, "bold"), fg="white", bd=0,
                           bg=color, activebackground=self.darken_color(color),
                           activeforeground="white", cursor="hand2", padx=15, pady=12,
                           relief=tk.RAISED)
            btn.pack(fill=tk.X)
            
            # Enhanced hover effects
            btn.bind("<Enter>", lambda e, btn=btn, color=color: 
                     btn.configure(bg=self.darken_color(color)))
            btn.bind("<Leave>", lambda e, btn=btn, color=color: 
                     btn.configure(bg=color))
        
        # Status bar at bottom with improved styling
        status_bar = tk.Label(self.window, text="System ready • Last access: 09 Apr 2025, 10:23 AM", 
                             bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=15, pady=6,
                             font=("Segoe UI", 9), bg="#ecf0f1", fg="#7f8c8d")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def darken_color(self, hex_color):
        """Darken hex color by 20% for hover effect"""
        # Convert hex to RGB
        h = hex_color.lstrip('#')
        r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        
        # Darken by 20%
        factor = 0.8
        r, g, b = int(r*factor), int(g*factor), int(b*factor)
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def brighten_color(self, hex_color):
        """Brighten hex color by 15% for hover effect"""
        # Convert hex to RGB
        h = hex_color.lstrip('#')
        r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        
        # Brighten by 15%
        factor = 1.15
        r = min(255, int(r*factor))
        g = min(255, int(g*factor))
        b = min(255, int(b*factor))
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def open_register_ui(self):
        RegisterUI(self.window, self.db, self.fr_system).show()

    def train_system(self):
        try:
            self.fr_system.train_model()
            messagebox.showinfo("Training Complete", "Face recognition system trained successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {e}")

    def monitor_gate(self):
        try:
            count = self.fr_system.monitor_gate()
            messagebox.showinfo("Monitoring Result", f"{count} known/unknown face(s) detected.")
        except Exception as e:
            messagebox.showerror("Error", f"Monitoring failed: {e}")

    def view_access_history(self):
        HistoryUI(self.window, self.db).show()