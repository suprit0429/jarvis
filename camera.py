import cv2
import time
import os

def capture_photo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera could not be opened.")
        return "Camera error"

    print("Get ready! Taking photo in 3 seconds...")
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)

    # Warm-up camera
    for _ in range(10):
        cap.read()

    ret, frame = cap.read()
    if ret:
        os.makedirs("captured_images", exist_ok=True)
        filename = f"captured_images/image_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print("Photo captured!")
        cv2.imshow("Captured Image", frame)
        cv2.waitKey(1000)  # Show preview for 1 second
        cv2.destroyAllWindows()
        cap.release()
        return "Photo captured"
    else:
        print("Failed to capture image.")
        cap.release()
        return "Failed to capture image"


def record_video(duration=5): 
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera could not be opened.")
        return "Camera error"

    print("Get ready! Starting video recording in 3 seconds...")
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    os.makedirs("captured_videos", exist_ok=True)
    filename = f"captured_videos/video_{int(time.time())}.mp4"
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Recording...', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Video recorded!")
    return "Video recorded"
