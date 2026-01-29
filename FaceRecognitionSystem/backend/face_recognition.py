import cv2
import os
import time
import datetime
import numpy as np
from backend.utils import get_face_recognizer, get_images_and_labels
from backend.config import BASE_DIR, FACE_RECOGNITION

class FaceRecognitionSystem:
    def __init__(self, db_instance):
        self.db = db_instance
        self.cascade_path = FACE_RECOGNITION['cascade_file']
        self.training_file = os.path.join(BASE_DIR, 'dataset', 'CapturedFaces', 'Trainner.yml')
        self.confidence_threshold = FACE_RECOGNITION['confidence_threshold']
        self.poor_match_threshold = FACE_RECOGNITION['poor_match_threshold']
        self.samples_per_face = FACE_RECOGNITION['samples_per_face']
        
    def capture_training_images(self, name, user_id):
        """Capture training images for a user"""
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(self.cascade_path)
        sample_num = 0
        
        while True:
            ret, img = cam.read()
            if not ret:
                raise Exception("Camera error. Please check your camera.")
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                sample_num += 1
                # Save the captured face
                output_path = os.path.join(BASE_DIR, 'dataset', 'CapturedFaces')
                os.makedirs(output_path, exist_ok=True)  # Ensure directory exists

                cv2.imwrite(os.path.join(output_path, f"{name}.{user_id}.{sample_num}.jpg"), gray[y:y+h, x:x+w])
                
                # Show progress
                cv2.putText(img, f"Images Captured: {sample_num}/{self.samples_per_face}", 
                           (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Capturing Face', img)
                
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sample_num >= self.samples_per_face:
                break
                
        cam.release()
        cv2.destroyAllWindows()
        
        return sample_num
        
    def train_model(self):
        """Train the face recognition model"""
        # Check if CapturedFaces directory exists and has files
        if not os.path.exists(f'{BASE_DIR}/dataset/CapturedFaces') or len(os.listdir(f'{BASE_DIR}/dataset/CapturedFaces')) == 0:
            raise Exception("No training images found. Please capture images first.")
            
        # Get face recognizer
        recognizer = get_face_recognizer()
            
        # Get training data
        faces, ids = get_images_and_labels(f"{BASE_DIR}/dataset/CapturedFaces")
        
        if len(faces) == 0:
            raise Exception("No faces detected in training images.")
            
        # Train model
        recognizer.train(faces, np.array(ids))
        
        # Save the model
        recognizer.save(self.training_file)
        
        # Log training in database
        self.db.log_training(len(faces))
        
        return len(faces)
        
    def monitor_gate(self, max_runtime=None):
        """Monitor gate for authorized users"""
        # Use default runtime if not specified
        if max_runtime is None:
            from backend.config import MONITORING
            max_runtime = MONITORING['default_duration']
            
        # Check if trained model exists
        if not os.path.exists(self.training_file):
            raise Exception("Trained model not found. Please train first.")
            
        # Initialize face recognizer
        recognizer = get_face_recognizer()
        
        # Load trained model
        recognizer.read(self.training_file)
        faceCascade = cv2.CascadeClassifier(self.cascade_path)
        
        # Start camera
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Track recognized users
        recognized_users = []
        
        # Set up timer
        start_time = time.time()
        
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        while True:
            ret, im = cam.read()
            if not ret:
                raise Exception("Camera error. Please check your camera.")
                
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                user_id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                
                tt = "Unknown"  # Default text
                access_granted = False
                
                if conf < self.confidence_threshold:  # Good match
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    
                    # Get user details from database
                    user = self.db.get_user_details(user_id)
                    
                    if user:
                        name = user['name']
                        id_number = user['id_number']
                        
                        # Get access count
                        access_count = self.db.get_access_count(user_id)
                        
                        tt = f"{name} (ID: {id_number})"
                        access_granted = True
                        
                        # Record gate access if first time in this session
                        if user_id not in recognized_users:
                            recognized_users.append(user_id)
                            self.db.record_gate_access(user_id, date, timeStamp, "Granted")
                        
                        # Display access count on image
                        cv2.putText(im, f"Access Count: {access_count + 1}", (x, y - 10), font, 0.75, (0, 255, 0), 2)
                
                if conf > self.poor_match_threshold:  # Poor match
                    # Save unknown face
                          # Save the captured face
                    output_path = os.path.join(BASE_DIR, 'dataset', 'UnknownFaces')
                    os.makedirs(output_path, exist_ok=True)  # Ensure directory exists
                    
                    noOfFile = len(os.listdir(f'{BASE_DIR}/dataset/UnknownFaces')) + 1
                    cv2.imwrite(os.path.join(output_path,f"Image{noOfFile}.jpg"), im[y:y + h, x:x + w])
                    
                    # Log unknown access attempt
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    self.db.record_gate_access(None, date, timeStamp, "Denied")
                
                # Display name and access status on image
                cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
                status_color = (0, 255, 0) if access_granted else (0, 0, 255)
                status_text = "ACCESS GRANTED" if access_granted else "ACCESS DENIED"
                cv2.putText(im, status_text, (x, y + h + 30), font, 0.75, status_color, 2)
            
            cv2.imshow('Gate Access Monitor', im)
            
            # Auto-exit condition
            if time.time() - start_time > max_runtime:
                break
            
            if cv2.waitKey(1) == ord('q'):  # Manual exit
                break
        
        cam.release()
        cv2.destroyAllWindows()
        
        # Log session in database
        duration = round(time.time() - start_time, 2)
        end_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.db.log_gate_session(current_date, end_time, len(recognized_users), duration)
        
        return len(recognized_users)