import cv2
import imutils

def detector(frame_queue, result_queue):
    prev_frame = None

    while True:
        frame = frame_queue.get()
        if frame is None:
            break

        gray_frame = frame
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray_frame
            result_queue.put({'frame': frame, 'contours': []})
            continue

        diff = cv2.absdiff(gray_frame, prev_frame)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        filtered_cnts = [c for c in cnts if cv2.contourArea(c) >= 500]

        prev_frame = gray_frame
        result_queue.put({'frame': frame, 'contours': filtered_cnts})
