import cv2
import serial
import time
import numpy as np
import nplds
# Connect to Arduino
arduino = serial.Serial('COM12', 9600, timeout=1)
time.sleep(2)

# ESP32-CAM stream URL
ESP32_STREAM_URL = "h......."

# Initialize the camera stream from ESP32
camera = cv2.VideoCapture(ESP32_STREAM_URL)

# Check if the camera is opened successfully
if not camera.isOpened():
    print("Error: Couldn't open the camera stream.")
    exit()

# Face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Servo angle limits
pan_min, pan_max = 70, 60
tilt_min, tilt_max = 60, 70

# Default servo positions
pan = 0;
tilt = 0;

while True:
    try:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1, 4)

        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_center_x = x + w // 2
            face_center_y = y + h // 2

            frame_center_x = frame.shape[1] // 2
            frame_center_y = frame.shape[0] // 2

            # Horizontal movement logic (instant left or right)
            if face_center_x < frame.shape[1] // 3:
                pan = pan_max  # Move fully left
            elif face_center_x > 2 * frame.shape[1] // 3:
                pan = pan_min  # Move fully right
            else:
                pan = 0  # Center

            # Vertical movement logic (instant up or down)
            if face_center_y < frame.shape[0] // 3:
                tilt = tilt_min  # Move fully up
            elif face_center_y > 2 * frame.shape[0] // 3:
                tilt = tilt_max  # Move fully down
            else:
                tilt = 0  # Center

            # Send command to Arduino
            command = f"{pan},{tilt}\n"
            arduino.write(command.encode('utf-8'))
            time.sleep(0.03)

            # Draw face box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 25, 0), 2)

        cv2.imshow("Face Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print("Error:", e)
        break

# Cleanup
camera.release()
cv2.destroyAllWindows()
arduino.close()
