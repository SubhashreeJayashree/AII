import cv2
import face_recognition
from db import load_face

def recognize_face(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    db_name, db_encoding = load_face()
    results = []

    for (top, right, bottom, left), enc in zip(locations, encodings):
        name = "Unknown"
        if db_encoding is not None:
            match = face_recognition.compare_faces([db_encoding], enc, 0.45)
            if match[0]:
                name = db_name
        results.append((top, right, bottom, left, name))
    return results
