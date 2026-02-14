import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)


import cv2
from FaceRecognitionSystem.backend.face_recognition import FaceRecognitionSystem
from FaceRecognitionSystem.backend.dbModule import FaceRecognitionDB
from FaceRecognitionSystem.backend.config import DB_CONFIG

from NumberPlateSystem.utils.plate_recognition import extract_plate_text
from NumberPlateSystem.data.vehicle_database import verify_vehicle
from PIL import Image



class GateLogic:
    def __init__(self):
        db = FaceRecognitionDB(**DB_CONFIG)
        self.face_system = FaceRecognitionSystem(db)

    def process_frame(self, frame):
        """
        frame: OpenCV BGR frame
        Returns: dict with results
        """

        results = {
            "faces": [],
            "plates": [],
            "decision": "GRANTED",
            "reason": "All verified"
        }

        # ---------- FACE CHECK ----------
        temp_path = "temp_gate.jpg"
        cv2.imwrite(temp_path, frame)

        face_result = self.face_system.recognize_face_from_image(temp_path)

        if face_result["status"] != "KNOWN":
            results["decision"] = "DENIED"
            results["reason"] = "Unknown face detected"
        else:
            results["faces"].append(face_result["name"])

        # ---------- PLATE CHECK ----------
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plate = extract_plate_text(pil_image)

        if plate:
            results["plates"].append(plate)
            if not verify_vehicle(plate)["exists"]:
                results["decision"] = "DENIED"
                results["reason"] = "Unregistered vehicle detected"
        else:
            results["decision"] = "DENIED"
            results["reason"] = "No number plate detected"

        return results
