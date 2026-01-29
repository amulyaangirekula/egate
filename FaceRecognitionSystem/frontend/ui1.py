import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os
from datetime import datetime
from backend.utils import validate_email, validate_name, validate_id

class AccessHistoryUI:
    def __init__(self, parent, db_instance):
        self.parent = parent
        self.db = db_instance
        
    def show_history_window(self):
        """Display the access history window"""
        try:
            # Create a new window
            history_window = tk.Toplevel(self.parent)
            history_window.title("Gate Access History")
            history_window.geometry("1000x700")
            
            # Search & Filter Section
            filter_frame = tk.Frame(history_window)
            filter_frame.pack(fill=tk.X, padx=10, pady=5)

            # Date Filter
            tk.Label(filter_frame, text="Start Date:").grid(row=0, column=0, padx=5)
            start_date_entry = tk.Entry(filter_frame)
            start_date_entry.grid(row=0, column=1, padx=5)

            tk.Label(filter_frame, text="End Date:").grid(row=0, column=2, padx=5)
            end_date_entry = tk.Entry(filter_frame)
            end_date_entry.grid(row=0, column=3, padx=5)

            # User Search
            tk.Label(filter_frame, text="User ID/Name:").grid(row=0, column=4, padx=5)
            search_entry = tk.Entry(filter_frame)
            search_entry.grid(row=0, column=5, padx=5)

            # Status Filter
            tk.Label(filter_frame, text="Status:").grid(row=0, column=6, padx=5)
            status_combobox = ttk.Combobox(filter_frame, values=["All", "Granted", "Denied"])
            status_combobox.current(0)
            status_combobox.grid(row=0, column=7, padx=5)

            # Search Button
            search_button = tk.Button(filter_frame, text="Search", 
                            command=lambda: self.refresh_tree(tree, start_date_entry.get(), 
                                                        end_date_entry.get(), 
                                                        search_entry.get(), 
                                                        status_combobox.get()))
            search_button.grid(row=0, column=8, padx=5)

            # Treeview for Displaying Records
            frame = tk.Frame(history_window)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            columns = ("Name", "ID Number", "Date", "Time", "Status", "Access Count")
            tree = ttk.Treeview(frame, columns=columns, show="headings")

            # Define headings
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            # Add scrollbar
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.pack(fill=tk.BOTH, expand=True)

            # Export Button
            export_button = tk.Button(history_window, text="Export to CSV", 
                             command=lambda: self.export_to_csv(tree, columns), width=15)
            export_button.pack(pady=5)

            # Close Button
            close_button = tk.Button(history_window, text="Close", 
                            command=history_window.destroy, width=10)
            close_button.pack(pady=5)

            # Initial data load
            self.refresh_tree(tree, "", "", "", "All")

        except Exception as e:
            messagebox.showerror("Error", f"Error viewing access history: {e}")

    def refresh_tree(self, tree, start_date, end_date, search_term, status):
        """Refresh the treeview with filtered data"""
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)

        # Get data with filters
        access_history = self.db.get_filtered_gate_access(
            start_date,
            end_date,
            search_term,
            status
        )

        # Insert filtered data into Treeview
        for entry in access_history:
            tree.insert("", tk.END, values=(
                entry.get('name', 'Unknown'),
                entry.get('id_number', 'N/A'),
                entry.get('date', ''),
                entry.get('time', ''),
                entry.get('status', ''),
                entry.get('access_count', 0)
            ))
            
    def export_to_csv(self, tree, columns):
        """Export treeview data to CSV file in 'access_logs/' with date in the filename"""
        
        # Ensure the 'access_logs/' folder exists
        logs_dir = os.path.join(os.path.dirname(__file__), '..', 'access_logs')
        os.makedirs(logs_dir, exist_ok=True)

        # Create filename with current date
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(logs_dir, f"Access_History_{date_str}.csv")

        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(columns)  # Write headers
                for child in tree.get_children():
                    writer.writerow(tree.item(child)['values'])
            messagebox.showinfo("Export Successful", f"Data exported successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error exporting data: {e}")

class MainUI:
    def __init__(self, window, db_instance, face_recognition_system):
        self.window = window
        self.db = db_instance
        self.fr_system = face_recognition_system
        
        # UI variables
        self.txt_name = None
        self.txt_id = None
        self.txt_email = None
        self.message = None
        self.message2 = None
        
        # Initialize UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI components"""
        self.window.title("Face Recognition Gate Access System")
        self.window.configure(background='blue')
        self.window.geometry('1350x750')  # Set window size

        # Main title
        message_title = tk.Label(self.window, text="AI-Enhanced Gate Access Control System", 
                          bg="Green", fg="white", width=50, height=3, 
                          font=('times', 30, 'italic bold underline')) 
        message_title.place(x=200, y=20)

        # Name field
        lbl = tk.Label(self.window, text="Name", width=20, height=2, 
                fg="red", bg="yellow", font=('times', 15, 'bold')) 
        lbl.place(x=400, y=200)
        self.txt_name = tk.Entry(self.window, width=20, bg="yellow", 
                          fg="red", font=('times', 15, 'bold'))
        self.txt_name.place(x=700, y=215)

        # ID field
        lbl2 = tk.Label(self.window, text="ID Number", width=20, fg="red", 
                 bg="yellow", height=2, font=('times', 15, 'bold')) 
        lbl2.place(x=400, y=270)
        self.txt_id = tk.Entry(self.window, width=20, bg="yellow", 
                       fg="red", font=('times', 15, 'bold'))
        self.txt_id.place(x=700, y=285)

        # Email field
        lbl3 = tk.Label(self.window, text="Email", width=20, fg="red", 
                 bg="yellow", height=2, font=('times', 15, 'bold')) 
        lbl3.place(x=400, y=340)
        self.txt_email = tk.Entry(self.window, width=20, bg="yellow", 
                          fg="red", font=('times', 15, 'bold'))
        self.txt_email.place(x=700, y=355)

        # Notification area
        lbl4 = tk.Label(self.window, text="Notification:", width=20, fg="red", 
                 bg="yellow", height=2, font=('times', 15, 'bold underline')) 
        lbl4.place(x=400, y=410)
        self.message = tk.Label(self.window, text="", bg="yellow", fg="red", 
                        width=30, height=2, activebackground="yellow", 
                        font=('times', 15, 'bold')) 
        self.message.place(x=700, y=410)

        # Detection details area
        lbl5 = tk.Label(self.window, text="Access Details:", width=20, fg="red", 
                 bg="yellow", height=2, font=('times', 15, 'bold underline')) 
        lbl5.place(x=400, y=650)
        self.message2 = tk.Label(self.window, text="", fg="red", bg="yellow", 
                         activeforeground="green", width=30, height=2, 
                         font=('times', 15, 'bold')) 
        self.message2.place(x=700, y=650)

        # Clear buttons
        clearButton_name = tk.Button(self.window, text="Clear", command=self.clear_name, 
                              fg="red", bg="yellow", width=10, height=1, 
                              activebackground="Red", font=('times', 15, 'bold'))
        clearButton_name.place(x=950, y=215)

        clearButton_id = tk.Button(self.window, text="Clear", command=self.clear_id, 
                            fg="red", bg="yellow", width=10, height=1, 
                            activebackground="Red", font=('times', 15, 'bold'))
        clearButton_id.place(x=950, y=285)    

        clearButton_email = tk.Button(self.window, text="Clear", command=self.clear_email, 
                               fg="red", bg="yellow", width=10, height=1, 
                               activebackground="Red", font=('times', 15, 'bold'))
        clearButton_email.place(x=950, y=355)    

        clearAll = tk.Button(self.window, text="Clear All", command=self.clear_all, 
                      fg="red", bg="yellow", width=10, height=1, 
                      activebackground="Red", font=('times', 15, 'bold'))
        clearAll.place(x=1080, y=285)    

        # Action buttons
        takeImg = tk.Button(self.window, text="Register User", command=self.register_user, 
                     fg="red", bg="yellow", width=20, height=3, 
                     activebackground="Red", font=('times', 15, 'bold'))
        takeImg.place(x=150, y=500)

        trainImg = tk.Button(self.window, text="Train System", command=self.train_system, 
                      fg="red", bg="yellow", width=20, height=3, 
                      activebackground="Red", font=('times', 15, 'bold'))
        trainImg.place(x=450, y=500)

        monitorBtn = tk.Button(self.window, text="Monitor Gate", command=self.monitor_gate, 
                        fg="red", bg="yellow", width=20, height=3, 
                        activebackground="Red", font=('times', 15, 'bold'))
        monitorBtn.place(x=750, y=500)

        historyBtn = tk.Button(self.window, text="Access History", 
                       command=self.view_access_history, fg="red", bg="yellow", 
                       width=20, height=3, activebackground="Red", 
                       font=('times', 15, 'bold'))
        historyBtn.place(x=1050, y=500)

        quitWindow = tk.Button(self.window, text="Quit", command=self.window.destroy, 
                       fg="red", bg="yellow", width=10, height=2, 
                       activebackground="Red", font=('times', 15, 'bold'))
        quitWindow.place(x=1150, y=650)
        
    # Button action methods
    def clear_name(self):
        self.txt_name.delete(0, 'end')    
        self.message.configure(text="")

    def clear_id(self):
        self.txt_id.delete(0, 'end')    
        self.message.configure(text="")

    def clear_email(self):
        self.txt_email.delete(0, 'end')    
        self.message.configure(text="")

    def clear_all(self):
        self.clear_name()
        self.clear_id()
        self.clear_email()
        self.message.configure(text="")
        self.message2.configure(text="")
        
    def register_user(self):
        """Register a new user with face capture"""
        try:
            name = self.txt_name.get()
            id_number = self.txt_id.get()
            email = self.txt_email.get()
            
            # Validation
            if not validate_name(name):
                self.message.configure(text="Please enter a valid name (alphabets only)")
                return
            if not validate_id(id_number):
                self.message.configure(text="Please enter an ID Number")
                return
            if not validate_email(email):
                self.message.configure(text="Please enter a valid email address")
                return
            
            # Add user to database
            user_id = self.db.add_user(name, id_number, email)
            
            if not user_id:
                self.message.configure(text="Error registering user in database")
                return
                
            # Start capturing face images
            self.message.configure(text="Please look at the camera...")
            self.window.update()
            
            samples = self.fr_system.capture_training_images(name, user_id)
            
            self.message.configure(text=f"Registration completed for ID: {user_id}")
            self.message2.configure(text="Training needed for face recognition")
            
        except Exception as e:
            self.message.configure(text=f"Error: {str(e)}")
            print(f"Error registering user: {e}")
            
    def train_system(self):
        """Train the face recognition system"""
        try:
            self.message.configure(text="Training in progress...")
            self.window.update()
            
            faces_count = self.fr_system.train_model()
            
            self.message.configure(text=f"Training Complete: {faces_count} faces trained")
            
        except Exception as e:
            self.message.configure(text=f"Error: {str(e)}")
            print(f"Error training system: {e}")
            
    def monitor_gate(self):
        """Monitor the gate for face recognition"""
        try:
            self.message.configure(text="Monitoring gate... Press 'q' to stop.")
            self.window.update()
            
            recognized_count = self.fr_system.monitor_gate()
            
            if recognized_count == 0:
                self.message2.configure(text="No known face detected")
            else:
                self.message2.configure(text=f"{recognized_count} user(s) recognized")
                
        except Exception as e:
            self.message.configure(text=f"Error: {str(e)}")
            print(f"Error monitoring gate: {e}")
            
    def view_access_history(self):
        """Show access history window"""
        history_ui = AccessHistoryUI(self.window, self.db)
        history_ui.show_history_window()