import cv2

def detector(frame_queue, result_queue):
    # Load the background image
    background_path = "data/background.png"
    background = cv2.imread(background_path, cv2.IMREAD_GRAYSCALE)
    if background is None:
        raise ValueError("Error: Unable to open background image file")

    while True:
        frame = frame_queue.get()
        if frame is None:
            break

        gray_frame = frame

        # Calculate the absolute difference between the current frame and the background
        fg_mask = cv2.absdiff(gray_frame, background)
        
        # Threshold the mask to create a binary image
        _, fg_mask = cv2.threshold(fg_mask, 50, 255, cv2.THRESH_BINARY)
        
        # Morphological operations to clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

        # Find contours in the thresholded image (OpenCV 4.x returns two values)
        contours, _ = cv2.findContours(fg_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on area
        filtered_contours = [contour for contour in contours if cv2.contourArea(contour) >= 500]

        result_queue.put({'frame': frame, 'contours': filtered_contours})
