import cv2
import numpy as np

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Image Preprocessing (Convert bytes to image)
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def crop_face(image: np.ndarray, bbox):
    """
    Crop only the face from the image
    """
    x1, y1, x2, y2 = bbox
    return image[y1:y2, x1:x2]