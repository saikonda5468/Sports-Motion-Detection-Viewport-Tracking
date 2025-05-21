"""
Motion detection functions for the sports video analysis project.
"""

import cv2
import numpy as np

def detect_motion(frames, frame_idx, threshold=25, min_area=100):
    """
    Detect motion in the current frame by comparing with previous frame.

    Args:
        frames: List of video frames
        frame_idx: Index of the current frame
        threshold: Threshold for frame difference detection
        min_area: Minimum contour area to consider

    Returns:
        List of bounding boxes for detected motion regions
    """
    # We need at least 2 frames to detect motion
    if frame_idx < 1 or frame_idx >= len(frames):
        return []

    # Get the current and previous frames
    current_frame = frames[frame_idx]
    prev_frame = frames[frame_idx - 1]

    # Convert both frames to grayscale to simplify processing
    gray_curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and smooth minor differences
    gray_curr = cv2.GaussianBlur(gray_curr, (5, 5), 0)
    gray_prev = cv2.GaussianBlur(gray_prev, (5, 5), 0)

    # Calculate the absolute difference between the blurred grayscale frames
    diff = cv2.absdiff(gray_prev, gray_curr)

    # Apply a binary threshold to the difference image
    # Pixels with a difference above 'threshold' become white (255), others black (0)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    # Dilate the thresholded image to fill in small holes and join fragmented regions
    dilated = cv2.dilate(thresh, None, iterations=2)

    # Find external contours (connected white regions) in the binary image
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_boxes = []

    # For each contour found, check if its area is significant
    for cnt in contours:
        if cv2.contourArea(cnt) >= min_area:
            # Get the bounding rectangle for the contour
            x, y, w, h = cv2.boundingRect(cnt)
            # Add it to the list of detected motion boxes
            motion_boxes.append((x, y, w, h))

    # Return all bounding boxes representing detected motion
    return motion_boxes
