import numpy as np
# from deepface import DeepFace

def analyze_emotion(face_img: np.ndarray) -> str:
    """
    Analyze the emotion from the face image using DeepFace
    """
    try:
        return None
        analysis = DeepFace.analyze(face_img, actions=["emotion"], enforce_detection=False)
        return analysis
    except Exception as e:
        return "Unknown"