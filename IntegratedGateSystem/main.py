import tkinter as tk
import cv2
from PIL import Image, ImageTk
from gate_logic import GateLogic
import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)


class IntegratedGateUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrated Gate System")

        self.logic = GateLogic()
        self.cap = cv2.VideoCapture(0)

        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.status_label = tk.Label(root, text="Initializing...", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            results = self.logic.process_frame(frame)

            # Update decision text
            if results["decision"] == "GRANTED":
                self.status_label.config(
                    text="ACCESS GRANTED",
                    fg="green"
                )
            else:
                self.status_label.config(
                    text=f"ACCESS DENIED: {results['reason']}",
                    fg="red"
                )

            # Show camera feed
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)

        self.root.after(500, self.update_frame)  # every 500ms

    def on_close(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = IntegratedGateUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
