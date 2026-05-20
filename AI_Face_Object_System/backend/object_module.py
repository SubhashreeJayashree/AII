import cv2

CLASSES = [
    "background","aeroplane","bicycle","bird","boat",
    "bottle","bus","car","cat","chair","cow",
    "diningtable","dog","horse","motorbike","person",
    "pottedplant","sheep","sofa","train","tvmonitor"
]

net = cv2.dnn.readNetFromCaffe(
    "models/MobileNetSSD_deploy.prototxt",
    "models/MobileNetSSD_deploy.caffemodel"
)

def detect_objects(frame):
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)),
        0.007843, (300, 300), 127.5
    )
    net.setInput(blob)
    detections = net.forward()

    objects = []
    for i in range(detections.shape[2]):
        conf = detections[0, 0, i, 2]
        if conf > 0.5:
            idx = int(detections[0, 0, i, 1])
            objects.append(CLASSES[idx])
    return list(set(objects))
