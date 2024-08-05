import multiprocessing
from streamer import streamer
from detector import detector
from viewer import viewer
import cv2

if __name__ == "__main__":
    video_path = "C:/temp/axon_test/data/People6387.mp4"

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        exit(1)
    cap.release()

    frame_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    streamer_process = multiprocessing.Process(target=streamer, args=(video_path, frame_queue))
    detector_process = multiprocessing.Process(target=detector, args=(frame_queue, result_queue))
    viewer_process = multiprocessing.Process(target=viewer, args=(result_queue, fps))

    try:
        streamer_process.start()
        detector_process.start()
        viewer_process.start()

        streamer_process.join()
        frame_queue.put(None)  # Signal the end to the detector
        detector_process.join()
        result_queue.put(None)  # Signal the end to the viewer
        viewer_process.join()
    except KeyboardInterrupt:
        pass
    finally:
        if streamer_process.is_alive():
            streamer_process.terminate()
        if detector_process.is_alive():
            detector_process.terminate()
        if viewer_process.is_alive():
            viewer_process.terminate()

        frame_queue.close()
        result_queue.close()
