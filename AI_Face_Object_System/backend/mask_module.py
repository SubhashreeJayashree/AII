import cv2
import numpy as np
from tensorflow.keras.models import load_model

face_cascade = cv2.CascadeClassifier(
    "models/haarcascade_frontalface_default.xml"
)

mask_model = load_model("models/mask_detector.model")

def detect_mask(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    results = []

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        face = cv2.resize(face, (224, 224))
        face = face / 255.0
        face = face.reshape(1, 224, 224, 3)

        mask, no_mask = mask_model.predict(face)[0]
        label = "Mask" if mask > no_mask else "No Mask"
        results.append((x, y, w, h, label))
    return results
