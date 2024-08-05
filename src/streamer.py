import cv2
import time

def streamer(video_path, frame_queue):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        frame_queue.put(None)
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_time = 1.0 / fps

    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_queue.put(gray_frame)

        # Sleep to maintain the frame rate
        elapsed_time = time.time() - start_time
        sleep_time = max(0, frame_time - elapsed_time)
        time.sleep(sleep_time)

    cap.release()
    frame_queue.put(None)  # Signal the end of the stream
