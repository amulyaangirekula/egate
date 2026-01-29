# 🔐 AI-Based E-Gate Management System -  Automatic Number Plate Recognition

A Python-based application that automates vehicle entry management using **AI-powered license plate recognition** with **Gemini API**. This system is designed to enhance access control in places like collegs, offices etc.

## ⚙️ How It Works (Detailed)

This system uses a combination of AI, GUI design, and computer vision to automate vehicle access control. It consists of three main workflows:

---

### 1. 🖼️ Image Upload & Number Plate Recognition


#### Step-by-Step:
1. The user clicks **"📷 Upload Image"** and selects an image file (JPG, PNG, etc.).
2. The selected image is displayed in the image panel on the left side of the UI.
3. When the user clicks **"✅ Register Plate"** or **"🔍 Verify Plate"**, the image is:
   - Sent to **Gemini AI** via API.
   - A specially crafted prompt asks Gemini to extract **only the number plate text**.
4. Gemini returns just the plate number (e.g., "TS09EF1234").
5. Depending on the action:
   - If registering: the plate is stored in a local `registered_vehicles.json` file with a timestamp.
   - If verifying: the plate is checked against the existing entries in the JSON file.
6. A message is displayed on the results panel indicating:
   - ✅ "Registration Successful"
   - ✅ "Access Granted"
   - ❌ "Access Denied"
   - ⚠️ "Already Registered"

> 🧠 **AI Note:** Using Gemini AI improves accuracy over traditional OCR by handling blurry text, different fonts, and plate formats more robustly.

---

### 2. 📹 Live Camera-Based Verification

This feature allows hands-free, real-time number plate recognition using a webcam.

#### Step-by-Step:
1. The user clicks **"📹 Live Verify"**.
2. The system starts the **webcam feed** using OpenCV and begins capturing frames.
3. Every few seconds (based on `CAPTURE_INTERVAL` in `config.py`), a frame is:
   - Captured and sent to Gemini AI just like a static image.
   - The plate number is extracted.
4. The extracted number is then checked against the local database.
5. Based on the result:
   - ✅ Access is **granted** if a match is found.
   - ❌ Access is **denied** if not found.
6. Each result includes a timestamp and is displayed live in the results panel.
7. Clicking **"⏹️ Stop Live Verify"** stops the camera feed.

> ⚙️ Behind the scenes: The `camera.py` module continuously captures frames in a separate thread, ensuring the UI remains responsive.

---

### 3. 📋 Local Vehicle Database Management

All registered vehicles are stored locally for fast, offline-accessible verification.

#### How it works:
- Data is stored in `data/registered_vehicles.json` in the format:
  ```json
  [
    {
      "plate": "TS09EF1234",
      "registered_at": "2025-05-02 14:32:10"
    }
  ]


---

## 🔧 Features

- 📷 Upload or capture vehicle images via webcam
- 🧠 AI-based number plate extraction using Gemini
- ✅ Register and verify vehicles against a local database
- 📹 Real-time live verification using camera feed
- 📋 View all registered plates
- 🗑️ Clear/reset the current session
- 🖥️ User-friendly dark-themed GUI built with Tkinter

---

## 📁 Project Structure

```text
NumberPlateSystem/
│
├── main.py                    # Entry point of the application
├── config.py                  # Configuration file (API key, colors, paths)
├── requirements.txt           # Python dependencies list
│
├── ui/                        # UI-related files
│   ├── app.py                 # Main application window and layout
│   ├── styles.py              # Theme and style settings
│   ├── frames/                # GUI sections (header, image, buttons, results)
│   └── components.py          # Custom widgets like HoverButton
│
├── utils/                     # Utility modules
│   ├── plate_recognition.py   # Gemini AI integration for plate detection
│   ├── camera.py              # OpenCV webcam capture and control
│   └── image_processor.py     # Image resizing and conversion utilities
│
├── data/
│   └── registered_vehicles.json  # Local JSON database of registered plates
│
└── assets/
    └── logo.png               # Logo image used in the header
```

## 🖥️ Technologies Used

- **Python 3.x**
- **Tkinter** (for GUI)
- **OpenCV** (for webcam support)
- **Pillow** (for image processing)
- **Google Generative AI (Gemini API)** (for plate recognition)
- **JSON** (for local data storage)

---

## 🛠️ Setup Instructions

###  1. Clone the Repository

Clone the project repository and navigate to the project directory:

```bash
git clone https://github.com/ViswasSomapongu/cbit-egate-system.git
cd NumberPlateSystem
```
### 2. Install Dependencies
Make sure Python 3 is installed, then run:

```bash
pip install -r requirements.txt
```
### 3. Add Your Gemini API Key

Open the config.py file and paste your API key:

```bash
API_KEY = "your-api-key-here"
```

▶️ How to Run

```bash
python main.py
```


## 📬 Contact
Feel free to reach out for contributions, suggestions, or improvements!

## Authors

- [Viswas Somapongu](https://www.linkedin.com/in/viswas-somapongu/)
- [Yash Talpallikar](https://www.linkedin.com/in/yash-talpallikar/)