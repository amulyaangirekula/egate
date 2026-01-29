from flask import Flask, request, jsonify
from backend.dbModule import FaceRecognitionDB
from backend.face_recognition import FaceRecognitionSystem
from backend.utils import validate_email, validate_name, validate_id
from backend.config import DB_CONFIG, DIRECTORIES
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize database
try:
    db = FaceRecognitionDB(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
except Exception as e:
    print(f"Database initialization error: {e}")
    exit(1)

# Initialize face recognition system
face_recognition_system = FaceRecognitionSystem(db)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    id_number = data.get("id_number")

    # Input validation
    if not validate_name(name):
        return jsonify({"error": "Invalid name"}), 400
    if not validate_id(id_number):
        return jsonify({"error": "Invalid ID"}), 400
    if not validate_email(email):
        return jsonify({"error": "Invalid email"}), 400

    # Register user
    try:
        user_id = db.add_user(name, id_number, email)
        if not user_id:
            return jsonify({"error": "Database registration failed"}), 500


        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/capture-face", methods=["POST"])
def capture():
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        user = db.get_user_details(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        samples = face_recognition_system.capture_training_images(user['name'], user_id)

        if samples >= face_recognition_system.samples_per_face:
            return jsonify({"message": "Face data captured successfully!"})
        else:
            return jsonify({"error": "Face data capture failed. Please try again."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
