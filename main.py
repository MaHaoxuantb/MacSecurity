from deepface import DeepFace
import time
import cv2
import os

def useCam():
    # Open the default camera (usually index 0)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Allow the camera to warm up
    time.sleep(1)

    # Capture a single frame
    ret, frame = cap.read()

    # Save the captured frame as an image file
    cv2.imwrite("image_c.jpg", frame)

def verify():
    start_time = time.time()

    try:
        result = DeepFace.verify(
            img1_path = "my_portrait.jpeg", 
            img2_path = "image_c.jpg", 
            model_name = "ArcFace",
            detector_backend = "retinaface",
            distance_metric = "cosine",
            enforce_detection = False,
            anti_spoofing = True
        )
        print(result)
        print("Time taken: %s seconds" % (time.time() - start_time))
        if result["verified"]:
            print("The faces are of the same person.")
            return True
        else:
            print("The faces are of different people.")
            return False
    except Exception as e:
        if "Spoof detected" in str(e):
            print("Spoofing detected! Access denied.")
            return False
        else:
            print("An error occurred during verification:", str(e))
            return False

def main():
    while True:
        useCam()
        samePerson = verify()
        if samePerson:
            print("Access Granted")
        else:
            print("Access Denied")
            os.system('osascript -e \'tell application "System Events" to keystroke "q" using {control down, command down}\'')
            exit()
        time.sleep(2)

main()