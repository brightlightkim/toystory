# import cv2
# import numpy as np
# import mediapipe as mp
# from deepface import DeepFace
# By Ujjwal Gupta
# class MoodAnalyzer:
#     def __init__(self):
#         self.mp_face = mp.solutions.face_detection
#         self.face_detection = self.mp_face.FaceDetection(min_detection_confidence=0.5)

#     def analyze_emotions(self, frame: np.ndarray) -> str:
#         gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

#         face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#         faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#         for (x, y, w, h) in faces:
#             face_roi = rgb_frame[y:y + h, x:x + w]
#             try:
#                 result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
#                 return result[0]['dominant_emotion']
#             except Exception:
#                 continue
        
#         return "neutral"

#     def process_frame(self, frame):
#         emotion = self.analyze_emotions(frame)
#         display_text = f"Emotion: {emotion}"
#         cv2.putText(frame, display_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
#         return frame, emotion
