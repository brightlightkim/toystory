''' 
    Instruction by Ujjwal Gupta, for local testing in directory,
    uncomment everything in this file. [Make sure to have have the image in the same directory]
    Run the file and open the browser to the localhost address.
    To test the API, use the following code:

    pip install -r requirements.txt
    
    run command: gunicorn main:app

    [for testing purposes] to input the image, use the following code in new terminal: 
    
    curl -X POST http://127.0.0.1:8000/process_image \ -F "image=@test.jpg"

    [make sure to have the image in the same directory]

'''
import cv2
import numpy as np
import mediapipe as mp
from deepface import DeepFace
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import base64
# import os
# from datetime import datetime

app = Flask(__name__)
api = Api(app)

# OUTPUT_DIR = "processed_images"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, min_detection_confidence=0.5)

EMOTION_MAP = {
    "angry": -2,
    "sad": -1,
    "neutral": 0,
    "happy": 2
}

EYE_INDICES = [33, 133, 362, 263, 7, 8, 9, 10, 226, 445]
LIP_INDICES = [61, 185, 40, 39, 37, 267, 269, 270, 409]
FACE_EDGES = [1, 4, 234, 454, 152]

class MoodAnalyzer:
    def analyze_emotions(self, image: np.ndarray) -> int:
        try:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = DeepFace.analyze(rgb_image, actions=['emotion'], enforce_detection=False)
            detected_emotion = result[0]['dominant_emotion'].lower()  
            return EMOTION_MAP.get(detected_emotion, 0)
        except Exception as e:  
            print(f"Error in emotion analysis: {str(e)}")
            return 0

mood_analyzer = MoodAnalyzer()

def draw_vectors(image, points, indices):
    for i in range(len(indices) - 1):
        p1 = points[indices[i]]
        p2 = points[indices[i+1]]
        cv2.line(image, p1, p2, (255, 0, 0), 1)

# def save_processed_image(image):
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"processed_image_{timestamp}.jpg"
#     filepath = os.path.join(OUTPUT_DIR, filename)
#     cv2.imwrite(filepath, image)
#     return filepath

class ProcessImage(Resource):
    def post(self):
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
            
        file = request.files['image']
        image_np = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image file"}), 400

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
        emotion_numeric = mood_analyzer.analyze_emotions(image)
        
        try:
            results = face_mesh.process(rgb_image) if emotion_numeric != 0 else None
            
            if results and results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    points = []
                    
                    for landmark in face_landmarks.landmark:
                        x = int(landmark.x * image.shape[1])
                        y = int(landmark.y * image.shape[0])
                        points.append((x, y))
                        cv2.circle(image, (x, y), 2, (255, 0, 0), -1)
                    
                    draw_vectors(image, points, EYE_INDICES)
                    draw_vectors(image, points, LIP_INDICES)
                    draw_vectors(image, points, FACE_EDGES)
            
            # saved_filepath = save_processed_image(image)
            
            _, buffer = cv2.imencode('.jpg', image)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return jsonify({
                "emotion_numeric": emotion_numeric,
                "image_base64": image_base64
              # ,"saved_filepath": saved_filepath
            })
            
        except Exception as e:
            return jsonify({"error": f"Error processing image: {str(e)}"}), 500

api.add_resource(ProcessImage, '/process_image')

if __name__ == '__main__':
    app.run(debug=True)