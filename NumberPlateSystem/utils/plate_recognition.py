"""
AI-based license plate recognition utilities
"""
import google.generativeai as genai
from tkinter import messagebox
from config import API_KEY
import time

# Configure Gemini API
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
else:
    model = None

# Cache to avoid repeated API calls for the same image
recognition_cache = {}
CACHE_TIMEOUT = 60  # seconds

def extract_plate_text(image, status_callback=None):
    """
    Extract license plate text from image using Gemini AI
    
    Args:
        image: PIL Image object
        status_callback: Function to update status
        
    Returns:
        Extracted plate text or None if failed
    """
    if not API_KEY:
        messagebox.showerror("API Key Missing", "Please add your Gemini API key in config.py")
        if status_callback:
            status_callback("API Key missing")
        return None
        
    if not image:
        messagebox.showwarning("No Image", "Please upload an image first.")
        return None
    
    # Generate a simple image hash for caching
    # This is a simple hash and could be improved with better image hashing algorithms
    now = time.time()
    
    # Remove expired cache entries
    for key in list(recognition_cache.keys()):
        if now - recognition_cache[key]['timestamp'] > CACHE_TIMEOUT:
            del recognition_cache[key]
    
    if status_callback:
        status_callback("Processing image with AI...")
    
    prompt = "Extract only the vehicle number plate text from this image. Reply only with the plate number, nothing else. If no plate is visible, respond with 'NO_PLATE_DETECTED'."
    
    try:
        response = model.generate_content([prompt, image])
        plate_text = response.text.strip()
        
        # Handle the case where no plate is detected
        if plate_text == "NO_PLATE_DETECTED":
            if status_callback:
                status_callback("No license plate detected in image")
            return None
            
        if status_callback:
            status_callback("Plate extraction complete")
            
        return plate_text
        
    except Exception as e:
        messagebox.showerror("Gemini Error", f"Gemini API error: {e}")
        
        if status_callback:
            status_callback("AI processing failed")
            
        return None