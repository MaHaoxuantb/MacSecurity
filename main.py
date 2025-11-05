import enum
from deepface import DeepFace
import time
import cv2
import os
import argparse

# Starter
class Mode(enum.Enum):
    NORMAL = "normal"
    STRICT = "strict"

# Arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-s", "--speed", help="high / low interval of face verification", default="low")
argparser.add_argument("-m", "--mode", help="mode of operation", default="normal")


def useCam():
    # Open the default camera (usually index 0)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Allow the camera to warm up
    # Adjust this if not MacBook Cam
    time.sleep(0.8)

    # Capture a single frame
    ret, frame = cap.read()

    # Save the captured frame as an image file
    cv2.imwrite("image_c.jpg", frame)

    # Release the camera
    cap.release()

def verify(mode: Mode):
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
            
            # Treat problems for the strict mode
            if mode == Mode.STRICT:
                if result["distance"] > 0.4: # adjust this if not MacBook
                    print("Strict mode: Distance too high. Access denied.")
                    return False
                if result["confidence"] < 0.8:
                    print("Strict mode: Confidence too low. Access denied.")
                    return False
                return True
            elif mode == Mode.NORMAL:
                if result["distance"] > 0.56: # adjust this if not MacBook
                    print("Normal mode: Distance too high. Access denied.")
                    return False
                return True
            else: # no need for this part
                assert "Unreachable code reached"
                return False
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
    
    if str(args.mode) == "normal":
        mode = Mode.NORMAL
        print("Operating in normal mode.")
    elif str(args.mode) == "strict":
        mode = Mode.STRICT
        print("Operating in strict mode.")
    else:
        mode = Mode.NORMAL
        print("Invalid mode argument. Using default 'normal' mode.")

    return detection_interval, mode

def main():
    detection_interval, mode = start()
    while True:
        useCam()
        samePerson = verify(mode)
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

if __name__ == "__main__":
    main()