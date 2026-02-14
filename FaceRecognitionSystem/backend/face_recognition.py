import cv2
import os
import time
import datetime
import numpy as np

from FaceRecognitionSystem.backend.utils import (
    get_face_recognizer,
    get_images_and_labels
)
from FaceRecognitionSystem.backend.config import FACE_RECOGNITION


class FaceRecognitionSystem:
    def __init__(self, db_instance):
        self.db = db_instance

        # Paths from config
        self.cascade_path = FACE_RECOGNITION["cascade_file"]
        self.training_file = FACE_RECOGNITION["training_file"]

        # Thresholds
        self.confidence_threshold = FACE_RECOGNITION["confidence_threshold"]
        self.poor_match_threshold = FACE_RECOGNITION["poor_match_threshold"]
        self.samples_per_face = FACE_RECOGNITION["samples_per_face"]

    # -------------------------------------------------
    # CAPTURE TRAINING IMAGES
    # -------------------------------------------------

    def capture_training_images(self, name, user_id):
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(self.cascade_path)

        if detector.empty():
            raise Exception(
                f"Haar cascade not loaded: {self.cascade_path}"
            )

        sample_num = 0
        output_path = os.path.dirname(self.training_file)
        os.makedirs(output_path, exist_ok=True)

        while True:
            ret, img = cam.read()
            if not ret:
                raise Exception("Camera error")

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                sample_num += 1

                cv2.imwrite(
                    os.path.join(
                        output_path,
                        f"{name}.{user_id}.{sample_num}.jpg"
                    ),
                    gray[y:y + h, x:x + w]
                )

                cv2.rectangle(
                    img, (x, y), (x + w, y + h), (255, 0, 0), 2
                )

                cv2.putText(
                    img,
                    f"Captured: {sample_num}/{self.samples_per_face}",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.imshow("Capturing Face", img)

            if cv2.waitKey(100) & 0xFF == ord("q"):
                break
            if sample_num >= self.samples_per_face:
                break

        cam.release()
        cv2.destroyAllWindows()
        return sample_num

    # -------------------------------------------------
    # TRAIN MODEL
    # -------------------------------------------------

    def train_model(self):
        training_dir = os.path.dirname(self.training_file)

        if not os.path.exists(training_dir) or len(os.listdir(training_dir)) == 0:
            raise Exception("No training images found")

        recognizer = get_face_recognizer()
        faces, ids = get_images_and_labels(training_dir)

        if len(faces) == 0:
            raise Exception("No faces detected in training data")

        recognizer.train(faces, np.array(ids))
        recognizer.save(self.training_file)

        self.db.log_training(len(faces))
        return len(faces)

    # -------------------------------------------------
    # SINGLE IMAGE RECOGNITION (INTEGRATED GATE)
    # -------------------------------------------------

    def recognize_face_from_image(self, image_path):
        if not os.path.exists(self.training_file):
            return {"status": "UNKNOWN", "name": None}

        recognizer = get_face_recognizer()
        recognizer.read(self.training_file)

        face_cascade = cv2.CascadeClassifier(self.cascade_path)
        if face_cascade.empty():
            raise Exception(
                f"Haar cascade not loaded: {self.cascade_path}"
            )

        img = cv2.imread(image_path)
        if img is None:
            return {"status": "UNKNOWN", "name": None}

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        if len(faces) == 0:
            return {"status": "UNKNOWN", "name": None}

        for (x, y, w, h) in faces:
            user_id, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < self.confidence_threshold:
                user = self.db.get_user_details(user_id)
                if user:
                    return {
                        "status": "KNOWN",
                        "name": user["name"]
                    }

        return {"status": "UNKNOWN", "name": None}

    # -------------------------------------------------
    # LIVE GATE MONITOR (FACE-ONLY APP)
    # -------------------------------------------------

    def monitor_gate(self, max_runtime=20):
        if not os.path.exists(self.training_file):
            raise Exception("Train model first")

        recognizer = get_face_recognizer()
        recognizer.read(self.training_file)

        face_cascade = cv2.CascadeClassifier(self.cascade_path)
        if face_cascade.empty():
            raise Exception(
                f"Haar cascade not loaded: {self.cascade_path}"
            )

        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX

        recognized_users = []
        start_time = time.time()
        today = datetime.date.today().strftime("%Y-%m-%d")

        unknown_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(self.training_file),
                "..",
                "UnknownFaces"
            )
        )
        os.makedirs(unknown_dir, exist_ok=True)

        while True:
            ret, frame = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                user_id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                access_granted = False
                label = "Unknown"

                if conf < self.confidence_threshold:
                    user = self.db.get_user_details(user_id)
                    if user:
                        access_granted = True
                        label = user["name"]

                        if user_id not in recognized_users:
                            recognized_users.append(user_id)
                            now = datetime.datetime.now()
                            self.db.record_gate_access(
                                user_id,
                                today,
                                now.strftime("%H:%M:%S"),
                                "Granted"
                            )

                elif conf > self.poor_match_threshold:
                    filename = f"unknown_{int(time.time())}.jpg"
                    cv2.imwrite(
                        os.path.join(unknown_dir, filename),
                        frame[y:y + h, x:x + w]
                    )

                color = (0, 255, 0) if access_granted else (0, 0, 255)
                status = "GRANTED" if access_granted else "DENIED"

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(
                    frame,
                    f"{label} - {status}",
                    (x, y - 10),
                    font,
                    0.9,
                    color,
                    2
                )

            cv2.imshow("Face Gate Monitor", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            if time.time() - start_time > max_runtime:
                break

        cam.release()
        cv2.destroyAllWindows()

        duration = round(time.time() - start_time, 2)
        self.db.log_gate_session(
            today,
            datetime.datetime.now().strftime("%H:%M:%S"),
            len(recognized_users),
            duration
        )

        return len(recognized_users)
