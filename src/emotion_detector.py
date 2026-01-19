import cv2
import time
import csv
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
from deepface import DeepFace


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


cap = cv2.VideoCapture(0)


resource_path("models/haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    raise RuntimeError("Face cascade not loaded")


emotion_count = {
    "Happy": 0,
    "Sad": 0,
    "Angry": 0,
    "Normal": 0
}

last_emotion = "Normal"

csv_file = open("emotion_log.csv", "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Time", "Emotion"])


frame_skip = 4
frame_count = 0
start_time = time.time()


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]

        if frame_count % frame_skip == 0:
            try:
                
                face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face_rgb = cv2.resize(face_rgb, (224, 224))

                result = DeepFace.analyze(
                    img_path=face_rgb,
                    actions=["emotion"],
                    enforce_detection=True,
                    detector_backend="opencv"   # 🔥 FIX
                )

                raw = result[0]["dominant_emotion"]

                if raw == "happy":
                    last_emotion = "Happy"
                elif raw == "sad":
                    last_emotion = "Sad"
                elif raw == "angry":
                    last_emotion = "Angry"
                else:
                    last_emotion = "Normal"

                emotion_count[last_emotion] += 1
                csv_writer.writerow([
                    datetime.now().strftime("%H:%M:%S"),
                    last_emotion
                ])

            except:
                pass

       
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

       
        cv2.putText(
            frame,
            last_emotion,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 0, 0),
            2
        )

    
    fps = int(1 / (time.time() - start_time))
    start_time = time.time()
    cv2.putText(frame, f"FPS: {fps}", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    
    y = 60
    for emo, count in emotion_count.items():
        cv2.putText(frame, f"{emo}: {count}", (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        y += 25

    
    cv2.putText(frame, "Q : Quit", (20, y + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200,200,200), 2)
    cv2.putText(frame, "S : Screenshot", (20, y + 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200,200,200), 2)

    cv2.imshow("EmotionSense", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("s"):
        cv2.imwrite("screenshot.png", frame)


cap.release()
cv2.destroyAllWindows()
csv_file.close()


plt.figure(figsize=(8,5))
plt.bar(emotion_count.keys(), emotion_count.values())
plt.title("Emotion Summary")
plt.xlabel("Emotion")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
