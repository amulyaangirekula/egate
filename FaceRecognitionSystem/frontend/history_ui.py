import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv, os
from datetime import datetime
from tkcalendar import DateEntry  # You may need to install this: pip install tkcalendar
from frontend.theme import LABEL_STYLE, BUTTON_STYLE

class HistoryUI:
    def __init__(self, parent, db_instance):
        self.parent = parent
        self.db = db_instance

    def show(self):
        window = tk.Toplevel(self.parent)
        window.title("Access History")
        window.geometry("1100x750")
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
            header.create_line(0, i, 1100, i, fill=color)
        
        # Title overlay on gradient
        header.create_text(550, 50, text="📂 Access History Dashboard", 
                          font=("Segoe UI", 24, "bold"), fill="white")

        # Main content container
        main_frame = tk.Frame(window, bg="#f5f7fa", padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Stats summary cards
        stats_frame = tk.Frame(main_frame, bg="#f5f7fa")
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create a summary panel instead of stats cards
        summary_frame = tk.Frame(main_frame, bg="white", padx=20, pady=15)
        summary_frame.pack(fill=tk.X, pady=(0, 15))
        summary_frame.configure(highlightbackground="#dcdde1", highlightthickness=1)

        # Add a header
        header_frame = tk.Frame(summary_frame, bg="white")
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Dashboard title with date
        current_date = datetime.now().strftime("%b %d, %Y")
        tk.Label(header_frame, text="Access Summary", font=("Segoe UI", 14, "bold"), 
                bg="white", fg="#2c3e50").pack(side=tk.LEFT)
        tk.Label(header_frame, text=f"As of {current_date}", font=("Segoe UI", 10), 
                bg="white", fg="#7f8c8d").pack(side=tk.RIGHT)

        # Add a horizontal separator
        separator = ttk.Separator(summary_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=5)

        # Add a welcome message or status overview
        message_frame = tk.Frame(summary_frame, bg="white", pady=10)
        message_frame.pack(fill=tk.X)

        tk.Label(message_frame, 
                text="Welcome to the access history dashboard. Use the filters below to search through records.",
                font=("Segoe UI", 11), bg="white", fg="#34495e", justify=tk.LEFT).pack(anchor="w")
        
        # Configure column weights for stats
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)
        
        # Filter Section with better styling
        filter_container = tk.Frame(main_frame, bg="white", padx=20, pady=15)
        filter_container.pack(fill=tk.X, pady=(0, 15))
        filter_container.configure(highlightbackground="#dcdde1", highlightthickness=1)
        
        # Filter title
        tk.Label(filter_container, text="Filter Access Records", 
                font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50").pack(anchor="w", pady=(0, 10))
        
        filter_frame = tk.Frame(filter_container, bg="white")
        filter_frame.pack(fill=tk.X)
        
        # Date filters
        date_frame = tk.Frame(filter_frame, bg="white")
        date_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        tk.Label(date_frame, text="Date Range", font=("Segoe UI", 11), 
                bg="white", fg="#34495e").pack(anchor="w", pady=(0, 5))
        
        date_inputs = tk.Frame(date_frame, bg="white")
        date_inputs.pack(fill=tk.X)
        
        # Use DateEntry for better date selection
        tk.Label(date_inputs, text="From:", font=("Segoe UI", 10), 
                bg="white", fg="#7f8c8d").grid(row=0, column=0, padx=(0, 5))
        start_date = DateEntry(date_inputs, width=12, background="#3498db", foreground="white", 
                              borderwidth=0, date_pattern="yyyy-mm-dd")
        start_date.grid(row=0, column=1, padx=5)
        
        tk.Label(date_inputs, text="To:", font=("Segoe UI", 10), 
                bg="white", fg="#7f8c8d").grid(row=0, column=2, padx=(10, 5))
        end_date = DateEntry(date_inputs, width=12, background="#3498db", foreground="white", 
                            borderwidth=0, date_pattern="yyyy-mm-dd")
        end_date.grid(row=0, column=3, padx=5)
        
        # User filter
        user_frame = tk.Frame(filter_frame, bg="white")
        user_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15)
        
        tk.Label(user_frame, text="User Filter", font=("Segoe UI", 11), 
                bg="white", fg="#34495e").pack(anchor="w", pady=(0, 5))
        
        search_frame = tk.Frame(user_frame, bg="white")
        search_frame.pack(fill=tk.X)
        
        search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), bd=1, relief=tk.SOLID)
        search_entry.pack(side=tk.LEFT, ipady=4, ipadx=5)
        search_entry.insert(0, "Enter name or ID")
        search_entry.config(fg="#95a5a6")
        
        # Add placeholder behavior
        def on_entry_click(event):
            if search_entry.get() == "Enter name or ID":
                search_entry.delete(0, tk.END)
                search_entry.config(fg="#2c3e50")
        
        def on_focusout(event):
            if search_entry.get() == '':
                search_entry.insert(0, "Enter name or ID")
                search_entry.config(fg="#95a5a6")
        
        search_entry.bind('<FocusIn>', on_entry_click)
        search_entry.bind('<FocusOut>', on_focusout)
        
        # Status filter
        status_frame = tk.Frame(filter_frame, bg="white")
        status_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15)
        
        tk.Label(status_frame, text="Access Status", font=("Segoe UI", 11), 
                bg="white", fg="#34495e").pack(anchor="w", pady=(0, 5))
        
        # Improved combobox styling
        style = ttk.Style()
        style.configure('TCombobox', padding=5)
        
        status_box = ttk.Combobox(status_frame, values=["All", "Granted", "Denied"], 
                                 width=12, font=("Segoe UI", 10))
        status_box.current(0)
        status_box.pack(ipady=1)
        
        # Buttons
        buttons_frame = tk.Frame(filter_frame, bg="white")
        buttons_frame.pack(side=tk.RIGHT, padx=15)
        
        # Apply filters button
        search_btn = tk.Button(buttons_frame, text="Apply Filters", font=("Segoe UI", 10, "bold"), 
                             bg="#3498db", fg="white", padx=15, pady=5, bd=0)
        search_btn.pack(side=tk.TOP, pady=(20, 5))
        
        # Reset filters button
        reset_btn = tk.Button(buttons_frame, text="Reset", font=("Segoe UI", 10), 
                             bg="#ecf0f1", fg="#34495e", padx=15, pady=5, bd=0)
        reset_btn.pack(side=tk.TOP)
        
        # Table Section with improved styling
        table_container = tk.Frame(main_frame, bg="white", padx=20, pady=15)
        table_container.pack(fill=tk.BOTH, expand=True)
        table_container.configure(highlightbackground="#dcdde1", highlightthickness=1)
        
        # Add title and info for the table
        table_header = tk.Frame(table_container, bg="white")
        table_header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(table_header, text="Access Records", 
                font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50").pack(side=tk.LEFT)
        
        # Table with better styling
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#f5f7fa")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        
        # Create a frame for the table and scrollbar
        tree_frame = tk.Frame(table_container, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Name", "ID Number", "Date", "Time", "Status", "Access Count", "Location")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        
        # Configure column widths better
        tree.column("Name", width=180)
        tree.column("ID Number", width=120)
        tree.column("Date", width=100)
        tree.column("Time", width=80)
        tree.column("Status", width=80)
        tree.column("Access Count", width=100)
        tree.column("Location", width=180)
        
        # Add vertical scrollbar
        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=y_scroll.set)
        y_scroll.pack(side="right", fill="y")
        
        # Add horizontal scrollbar
        x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=x_scroll.set)
        x_scroll.pack(side="bottom", fill="x")
        
        tree.pack(fill="both", expand=True)
        
        # Add some sample data for demonstration
        sample_data = [
            ("John Smith", "EMP001", "2025-04-08", "09:15", "Granted", "127", "Main Entrance"),
            ("Sarah Johnson", "EMP042", "2025-04-08", "09:27", "Granted", "85", "Side Gate"),
            ("Michael Brown", "EMP019", "2025-04-08", "09:43", "Granted", "210", "Main Entrance"),
            ("Emma Wilson", "VIS012", "2025-04-08", "10:02", "Denied", "3", "Parking Entrance"),
            ("David Lee", "EMP031", "2025-04-08", "10:15", "Granted", "156", "Side Gate"),
            ("Jennifer Parker", "EMP027", "2025-04-08", "10:27", "Granted", "94", "Main Entrance"),
            ("Robert Taylor", "CON003", "2025-04-08", "10:34", "Granted", "12", "Loading Dock"),
            ("Lisa Anderson", "EMP055", "2025-04-08", "10:49", "Granted", "201", "Main Entrance"),
            ("James Wilson", "VIS008", "2025-04-08", "11:05", "Denied", "1", "Main Entrance"),
            ("Patricia Garcia", "EMP013", "2025-04-08", "11:12", "Granted", "178", "Side Gate"),
        ]
        
        for person in sample_data:
            tree.insert("", tk.END, values=person)
            
        # Color code the status column
        for item in tree.get_children():
            if tree.item(item)["values"][4] == "Granted":
                tree.tag_configure("granted", foreground="#2ecc71")
                tree.item(item, tags=("granted",))
            else:
                tree.tag_configure("denied", foreground="#e74c3c")
                tree.item(item, tags=("denied",))
                
        # Actions bar at the bottom
        actions_frame = tk.Frame(main_frame, bg="#f5f7fa", pady=15)
        actions_frame.pack(fill=tk.X)
        
        # Left side info
        info_label = tk.Label(actions_frame, text="Showing 10 records", 
                            font=("Segoe UI", 10), bg="#f5f7fa", fg="#7f8c8d")
        info_label.pack(side=tk.LEFT)
        
        # Right side action buttons
        export_btn = tk.Button(actions_frame, text="Export to CSV", font=("Segoe UI", 10, "bold"), 
                              bg="#3498db", fg="white", padx=15, pady=8, bd=0)
        export_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        print_btn = tk.Button(actions_frame, text="Print Report", font=("Segoe UI", 10), 
                             bg="#ecf0f1", fg="#34495e", padx=15, pady=8, bd=0)
        print_btn.pack(side=tk.RIGHT)
        
        # Function definitions
        def refresh():
            tree.delete(*tree.get_children())
            
            # Get filter values
            start = start_date.get_date().strftime('%Y-%m-%d')
            end = end_date.get_date().strftime('%Y-%m-%d')
            search = search_entry.get()
            if search == "Enter name or ID":
                search = ""
            status = status_box.get()
            
            data = self.db.get_filtered_gate_access(start, end, search, status)
            for entry in data:
                values = (
                    entry.get("name", ""),
                    entry.get("id_number", ""),
                    entry.get("date", ""),
                    entry.get("time", ""),
                    entry.get("status", ""),
                    entry.get("access_count", 0),
                    entry.get("location", "N/A")  # Added location
                )
                item_id = tree.insert("", tk.END, values=values)
                
                # Color code based on status
                if entry.get("status") == "Granted":
                    tree.tag_configure("granted", foreground="#2ecc71")
                    tree.item(item_id, tags=("granted",))
                else:
                    tree.tag_configure("denied", foreground="#e74c3c")
                    tree.item(item_id, tags=("denied",))
            
            # Update info label
            info_label.config(text=f"Showing {len(data)} records")

        def reset_filters():
            # Reset date entries to today
            today = datetime.now().date()
            start_date.set_date(today)
            end_date.set_date(today)
            
            # Reset search field
            search_entry.delete(0, tk.END)
            search_entry.insert(0, "Enter name or ID")
            search_entry.config(fg="#95a5a6")
            
            # Reset status
            status_box.current(0)
            
            # Refresh the data
            refresh()

        def export():
            path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"Access_History_{datetime.now().strftime('%Y-%m-%d')}.csv"
            )
            
            if path:
                try:
                    with open(path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(columns)
                        for child in tree.get_children():
                            writer.writerow(tree.item(child)['values'])
                    messagebox.showinfo("Success", f"Exported to {path}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        # Connect functions to buttons
        search_btn.config(command=refresh)
        reset_btn.config(command=reset_filters)
        export_btn.config(command=export)
        print_btn.config(command=lambda: messagebox.showinfo("Print", "Sending to printer..."))
        
        # Add hover effects to buttons
        def on_enter(event, button, bg, fg):
            button.config(background=bg, foreground=fg)
            
        def on_leave(event, button, bg, fg):
            button.config(background=bg, foreground=fg)
        
        search_btn.bind("<Enter>", lambda event: on_enter(event, search_btn, "#2980b9", "white"))
        search_btn.bind("<Leave>", lambda event: on_enter(event, search_btn, "#3498db", "white"))
        
        reset_btn.bind("<Enter>", lambda event: on_enter(event, reset_btn, "#dcdde1", "#2c3e50"))
        reset_btn.bind("<Leave>", lambda event: on_enter(event, reset_btn, "#ecf0f1", "#34495e"))
        
        export_btn.bind("<Enter>", lambda event: on_enter(event, export_btn, "#2980b9", "white"))
        export_btn.bind("<Leave>", lambda event: on_enter(event, export_btn, "#3498db", "white"))
        
        print_btn.bind("<Enter>", lambda event: on_enter(event, print_btn, "#dcdde1", "#2c3e50"))
        print_btn.bind("<Leave>", lambda event: on_enter(event, print_btn, "#ecf0f1", "#34495e"))