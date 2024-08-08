import numpy as np
from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *
import time
import requests
import threading

video_path = 'WhatsApp Video 2024-08-05 at 10.01.12_281b1a61.mp4'  # Replace with your video file path or 0 for webcam
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

phone = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog",
    "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
    "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich",
    "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa",
    "pottedplant", "bed", "diningtable", "toilet", "TV monitor", "laptop", "mouse", "remote",
    "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use 'XVID' for .avi files
out = cv2.VideoWriter("output_video_path.mp4", fourcc, fps, (frame_width, frame_height))

idx = phone.index("cell phone")

def dataGet(ra):
    data = {
      "subjectID": 1,
      "rating": ra
    }

    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IkNTMTIzIiwidXNlcl90eXBlIjoic3RhZmYiLCJleHAiOjE3NTQ0NDk2Mzh9.OsIlhB88ZZMHK9_tlI06E3J2D3r4Alj14OopsUfLmVM",  # Replace with your actual token
        "Content-Type": "application/json"
    }

    response = requests.post("http://localhost:8000/api/features/interaction/", json=data, headers=headers)

    print(f"Status Code: {response.status_code}")

model = YOLO('./run3/train/weights/best.pt')
model2 = YOLO("./yolov8l.pt")

prev = 0
classNames = {
    0: 'hand-raising',
    1: 'reading',
    2: 'writing'
}
start_time = time.time()
arr = []
# Tracking
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
num_inter = 0

def detect_phone(img, results2):
    for r in results2:
        boxes = r.boxes
        for box in boxes:
            if int(box.cls[0]) == idx:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

                # Confidence
                conf = math.ceil((box.conf[0] * 100)) / 100
                # Class Name
                cls = int(box.cls[0])
                currentClass = phone[cls]

                if conf > 0.5:
                    cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5)
                    cvzone.putTextRect(img, f'{currentClass} {conf}', (max(0, x1), max(35, y1)),
                                       scale=2, thickness=2, offset=2)

def detect_actions(img, results):
    global detections
    detections = np.empty((0, 5))
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if conf > 0.5:
                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5)
                cvzone.putTextRect(img, f'{currentClass} {conf}', (max(0, x1), max(35, y1)),
                                   scale=2, thickness=2, offset=2)
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))

while True:
    success, img = cap.read()
    if not success:
        break

    results = model(img, stream=True)
    results2 = model2(img, stream=True)

    phone_thread = threading.Thread(target=detect_phone, args=(img, results2))
    actions_thread = threading.Thread(target=detect_actions, args=(img, results))

    phone_thread.start()
    actions_thread.start()

    phone_thread.join()
    actions_thread.join()

    resultsTracker = tracker.update(detections)
    for result in resultsTracker:
        x1, y1, x2, y2, id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        print(result)
        w, h = x2 - x1, y2 - y1
        num_inter = max(num_inter, int(id))
    print(num_inter, arr)

    elapsed_time = time.time() - start_time
    if elapsed_time > 30:
        print(f"Maximum interactions in last 30 seconds: {num_inter}")
        arr.append(num_inter - prev)
        tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
        prev = num_inter
        start_time = time.time()

    cv2.imshow("Image", img)
    out.write(img)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()
