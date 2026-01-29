# 🔐 AI-Based E-Gate Management System - Face Recognition System

A smart, secure, and offline face recognition-based gate access control system developed using **Python**, **OpenCV**, and **MySQL**. Built with a modular backend and a sleek **Tkinter-based GUI**.



## 💡 How It Works

### 👤 Registration
- Capture **60 face images** using a webcam.
- Save them with the **user's name and ID**.

### 🧠 Training
- Train an **LBPH (Local Binary Pattern Histogram)** model using OpenCV.
- Save the trained model to disk as `Trainner.yml`.

### 🚪 Monitoring
- Start the webcam.
- Detect faces in real-time.
- Compare each detected face with the trained model:
  - **Confidence < 50** → ✅ Known → **Access Granted**
  - **Confidence > 75** → ❌ Unknown → **Access Denied**
- Save intruder face images.
- Log all access attempts in the database.

### 📊 Dashboard
- View all logs in the **Access History** section.
- **Filter logs** by date, name, or access status.
- **Export logs to CSV**.
- See a **real-time visual dashboard** of access attempts.

---

## 🧠 Model Used

- **LBPH Face Recognizer**
  - Effective on small datasets.
  - Fast and suitable for offline systems.
  - Uses **Local Binary Patterns** to extract facial features.
  
- **Detection**: Haar Cascade classifier (OpenCV)
- **Training Flow**:
  1. Convert face images to **grayscale**.
  2. Extract **histogram-based features**.
  3. Train and save the model to disk.

---

## 🛡️ Security Features

- ✅ **Offline & secure** — no internet/cloud dependency.
- 🔐 **Admin-only** access to training and access logs.
- 📸 **Stores unknown faces** for future training or review.




---

## 🚀 Features

- 📷 **Capture Training Images** — Take multiple face samples for each user.
- 🧠 **Train Recognition Model** — Uses LBPH algorithm to train on registered faces.
- 🎥 **Live Monitoring** — Recognizes faces in real-time and logs gate access.
- 🚫 **Intruder Detection** — Saves unknown faces and denies access.
- 🗄️ **Access Logging** — Stores detailed access history with timestamps.
- 📊 **Dashboard** — Filter, view, and export access records via a GUI.

---

## 📁 Project Structure

```text
FaceRecognitionSystem/
│
├── backend/
│   ├── dataset/
│   │   ├── CapturedFaces/           # Saved training face images
│   │   └── UnknownFaces/            # Saved unknown/intruder faces
│   │
│   ├── main.py                      # App entry point
│   ├── config.py                    # DB credentials and app config
│   ├── face_recognition.py          # Face detection, training, recognition logic
│   ├── dbModule.py                  # MySQL database handler
│   └── utils.py                     # Helper functions and validators
│
├── frontend/
│   ├── main_ui.py                   # Main dashboard GUI
│   ├── register_ui.py               # New user registration UI
│   ├── history_ui.py                # Access history and filter/export
│   └── theme.py                     # UI style definitions
│
├── assets/
│   └── haarcascade_frontalface_default.xml   # Haar Cascade model
│
├── access_logs/
│   └── Access_History_<date>.csv    # Daily access history logs
│
├── logo.png                         # App logo for UI
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation


```

---

## ⚙️ Requirements

- Python 3.8–3.11 (recommended)
- MySQL Server (localhost setup)

Install Python packages:

```bash
pip install -r requirements.txt

```

## 🛠️ Setup Instructions

### 🔧 1. Clone the Repository

Clone the project repository and navigate to the project directory:

```bash
git clone https://github.com/ViswasSomapongu/cbit-egate-system.git
cd FaceRecognitionSystem
```
### 🐬 2. Set Up MySQL
Ensure MySQL is installed and running. The system auto-creates the database and tables.

Edit backend/config.py and set your MySQL credentials:
```
DB_CONFIG = {
    'host': 'localhost',
    'user': 'yourusername',
    'password': 'yourpassword',
    'database': 'face_recognition'
}
```

### 📁 3. Ensure Required Files Exist
- assets/haarcascade_frontalface_default.xml
➤ Download from OpenCV.

- logo.png
➤ Place your project logo or remove the reference in frontend/main_ui.py.

- ▶️ Running the App
From the project root, run:
```
python -m backend.main
```
✅ Ensure the MySQL server is active before launching.





## 📬 Contact
Feel free to reach out for contributions, suggestions, or improvements!

## Authors

- [Viswas Somapongu](https://www.linkedin.com/in/viswas-somapongu/)
- [Yash Talpallikar](https://www.linkedin.com/in/yash-talpallikar/)

