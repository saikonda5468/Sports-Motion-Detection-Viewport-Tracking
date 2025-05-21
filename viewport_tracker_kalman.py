"""
Viewport tracking functions for creating a smooth "virtual camera".
"""

import cv2
import numpy as np
from filterpy.kalman import KalmanFilter

def calculate_region_of_interest(motion_boxes, frame_shape):
    """
    Calculate the primary region of interest based on motion boxes.

    Args:
        motion_boxes: List of motion detection bounding boxes
        frame_shape: Shape of the video frame (height, width)

    Returns:
        Tuple (x, y, w, h) representing the region of interest center point and dimensions
    """
    # If no motion is detected, use the center of the frame as the default ROI
    if not motion_boxes:
        height, width = frame_shape[:2]
        return (width // 2, height // 2, 0, 0)

    # Weighted average initialization
    total_area = 0
    weighted_x_sum = 0
    weighted_y_sum = 0

    # Iterate through all motion boxes and weight the centers by area
    for (x, y, w, h) in motion_boxes:
        area = w * h
        center_x = x + w // 2
        center_y = y + h // 2

        weighted_x_sum += center_x * area
        weighted_y_sum += center_y * area
        total_area += area

    # Compute the weighted average center of all motion regions
    avg_x = int(weighted_x_sum / total_area)
    avg_y = int(weighted_y_sum / total_area)

    return (avg_x, avg_y, 0, 0)

def initialize_kalman_filter():
    """
    Initialize a Kalman Filter with a constant velocity model for 2D tracking.

    Returns:
        A configured KalmanFilter object.
    """
    kf = KalmanFilter(dim_x=4, dim_z=2)  # State: [x, y, dx, dy]; Measurement: [x, y]

    # Define how the state evolves from frame to frame (assuming constant velocity)
    kf.F = np.array([[1, 0, 1, 0],
                     [0, 1, 0, 1],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

    # Define how the measurements relate to the state (we only observe x and y)
    kf.H = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0]])

    # Initial state covariance matrix (uncertainty)
    kf.P *= 1000.

    # Measurement noise covariance matrix (how noisy we expect measurements to be)
    kf.R *= 5.

    # Process noise covariance matrix (model uncertainty)
    kf.Q = np.eye(4) * 0.03

    return kf

def track_viewport(frames, motion_results, viewport_size):
    """
    Track viewport position across frames using Kalman filtering.

    Args:
        frames: List of video frames
        motion_results: List of motion detection results per frame
        viewport_size: Tuple (width, height) defining the size of the virtual camera window

    Returns:
        List of viewport center positions (x, y) for each frame.
    """
    viewport_positions = []

    # If no frames are available, return an empty list
    if not frames:
        return []

    # Get frame and viewport dimensions
    frame_height, frame_width = frames[0].shape[:2]
    half_w, half_h = viewport_size[0] // 2, viewport_size[1] // 2

    # Initialize Kalman filter
    kf = initialize_kalman_filter()

    for i in range(len(frames)):
        # Compute the center of motion activity (region of interest)
        cx, cy, _, _ = calculate_region_of_interest(motion_results[i], frames[i].shape)

        # Initialize Kalman filter state on the first frame
        if i == 0:
            kf.x = np.array([[cx], [cy], [0], [0]])  # [pos_x, pos_y, vel_x, vel_y]

        # Predict the next state (based on previous state and velocity)
        kf.predict()

        # Update the filter with the new observed center from motion detection
        kf.update(np.array([[cx], [cy]]))

        # Extract the filtered/smoothed viewport center
        smoothed_x = int(kf.x[0])
        smoothed_y = int(kf.x[1])

        # Ensure the viewport stays within the video frame boundaries
        smoothed_x = max(half_w, min(frame_width - half_w, smoothed_x))
        smoothed_y = max(half_h, min(frame_height - half_h, smoothed_y))

        # Save the final viewport center for this frame
        viewport_positions.append((smoothed_x, smoothed_y))

    return viewport_positions
