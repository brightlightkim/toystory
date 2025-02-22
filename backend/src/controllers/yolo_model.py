import cv2
import torch
import numpy as np
# from ultralytics import YOLO

# YOLO 모델 로드
# yolo_model = YOLO("yolov8n.pt")

def detect_faces(image: np.ndarray):
    """
    Use YOLOv8 to detect faces
    """
    # results = yolo_model(image)
    faces = []

    # for r in results:
    #     boxes = r.boxes
    #     for box in boxes:
    #         x1, y1, x2, y2 = map(int, box.xyxy[0])
    #         faces.append((x1, y1, x2, y2))

    return faces