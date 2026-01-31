"""
License plate recognition using OpenCV + Tesseract OCR (LIVE)
Contour-based plate detection (more reliable than Haar)
"""

import cv2
import numpy as np
import pytesseract
from collections import Counter

# IMPORTANT: Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Buffer to stabilize live OCR results
plate_buffer = []


def extract_plate_text(image, status_callback=None):
    """
    Extract license plate text from a live camera frame (PIL Image)

    Args:
        image: PIL Image captured from camera
        status_callback: Function to update UI status

    Returns:
        Final stabilized plate text or None
    """

    if image is None:
        return None

    try:
        if status_callback:
            status_callback("Detecting number plate...")

        # Convert PIL Image → OpenCV (BGR)
        img = np.array(image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Resize full frame slightly for better contour detection
        img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Noise reduction
        gray = cv2.bilateralFilter(gray, 11, 17, 17)

        # Edge detection
        edged = cv2.Canny(gray, 170, 200)

        # Find contours
        contours, _ = cv2.findContours(
            edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        # Sort contours by area (largest first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        plate_img = None

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)

            # Plate is usually rectangular (4 sides)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)

                # Aspect ratio check for number plates
                aspect_ratio = w / float(h)

                if 2.0 < aspect_ratio < 6.0 and w > 100 and h > 30:
                    plate_img = img[y:y + h, x:x + w]
                    break

        if plate_img is None:
            if status_callback:
                status_callback("No plate detected")
            return None

        # ---------- PREPROCESSING FOR OCR ----------
        plate_img = cv2.resize(
            plate_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC
        )

        gray_plate = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        gray_plate = cv2.bilateralFilter(gray_plate, 11, 17, 17)

        _, thresh = cv2.threshold(
            gray_plate, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # ---------- OCR ----------
        config = (
            "--oem 3 "
            "--psm 7 "
            "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )

        text = pytesseract.image_to_string(thresh, config=config)
        plate_text = text.strip().replace(" ", "").replace("\n", "")

        # Debug output (VERY useful)
        print("OCR RAW OUTPUT:", repr(text))

        if len(plate_text) < 6:
            if status_callback:
                status_callback("No plate detected")
            return None

        # ---------- LIVE STABILIZATION ----------
        plate_buffer.append(plate_text)

        if len(plate_buffer) >= 1:
            final_plate = Counter(plate_buffer).most_common(1)[0][0]
            plate_buffer.clear()

            print("FINAL PLATE:", final_plate)

            if status_callback:
                status_callback("Plate detected successfully")

            return final_plate

        return None

    except Exception as e:
        print("OCR ERROR:", e)
        if status_callback:
            status_callback("OCR failed")
        return None