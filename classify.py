# Import necessary libraries
from ultralytics import YOLO
import cv2
import numpy as np
import os
import json as json

# Here we use a pre-trained model from the YOLOv7 repository
model = YOLO('../weights/yolo11n.pt')  # You have to provide a compatible yolo model such as yolo11n.pt

def analyze(file: str):
    image = cv2.imread(file)

    # Perform object detection
    results = model(image)
    
    point_info = []
    for result in results:

        if hasattr(result, 'boxes'):
            for box, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
                x1, y1, x2, y2 = map(int, box.tolist())  # convert tensor to list

                class_name = model.names[int(cls)]
                ignore_objects = ('kite')

                # return only high confidence items
                if conf > 0.6:
                    if class_name not in ignore_objects: 
                        point = { 'class': class_name, 'confidence': float(conf), 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
                        point_info.append(point)
        else:
            print("Bounding boxes not found in model output.")

        return json.dumps(point_info)