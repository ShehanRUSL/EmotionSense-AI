import cv2


cap = cv2.VideoCapture(0)


if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

print("Webcam opens")
print("Live video appears")
print("Press Q to exit")


while True:
    ret, frame = cap.read()
    
    
    if not ret:
        print("Error: Failed to read frame")
        break

    
    cv2.imshow("Camera Test", frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break


cap.release()
cv2.destroyAllWindows()
print("Camera closed")
