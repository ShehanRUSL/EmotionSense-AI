import cv2

# Open the default webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

print("Webcam opens")
print("Live video appears")
print("Press Q to exit")

# Capture video frame by frame
while True:
    ret, frame = cap.read()
    
    # Check if frame was read successfully
    if not ret:
        print("Error: Failed to read frame")
        break

    # Display the frame
    cv2.imshow("Camera Test", frame)

    # Wait for Q key to exit (1ms delay between frames)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
print("Camera closed")
