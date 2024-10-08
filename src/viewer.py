import cv2
import time

def blur_region(frame, x, y, w, h):
    frame[y:y+h, x:x+w] = cv2.GaussianBlur(frame[y:y+h, x:x+w], (51, 51), 0)
    return frame

def viewer(result_queue, fps):
    frame_time = 1.0 / fps

    while True:
        start_time = time.time()
        data = result_queue.get()
        if data is None:
            break

        frame = data['frame']
        contours = data['contours']

        # Blur detected regions
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            frame = blur_region(frame, x, y, w, h)

        #time overlay
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255), 2, cv2.LINE_AA)

        cv2.imshow("Frame", frame)

        #maintain original frame rate
        elapsed_time = time.time() - start_time
        sleep_time = max(0, frame_time - elapsed_time)
        time.sleep(sleep_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
