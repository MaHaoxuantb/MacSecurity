from deepface import DeepFace
import time
import cv2
import os
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-s", "--speed", help="high / low interval of face verification", default="low")

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

def start():
    args = argparser.parse_args()
    if str(args.speed) == "high":
        detection_interval = 1
    elif str(args.speed) == "low":
        detection_interval = 5
    else:
        print("Invalid speed argument. Using default 'low' interval.")
        detection_interval = 5
    return detection_interval

def main():
    detection_interval = start()
    while True:
        useCam()
        samePerson = verify()
        if samePerson:
            print("Access Granted")
        else:
            print("Access Denied")
            if os.name == "nt":
                os.system("rundll32.exe user32.dll,LockWorkStation")
            else:
                os.system('osascript -e \'tell application "System Events" to keystroke "q" using {control down, command down}\'')
            exit()
        time.sleep(detection_interval)

main()