import cv2

def streamer(video_path, frame_queue):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        frame_queue.put(None)
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_queue.put(gray_frame)

    cap.release()
    frame_queue.put(None)  # Signal the end of the stream
