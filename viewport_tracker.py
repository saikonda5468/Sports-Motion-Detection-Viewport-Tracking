"""
Viewport tracking functions for creating a smooth "virtual camera".
"""

import cv2
import numpy as np


def calculate_region_of_interest(motion_boxes, frame_shape):
    """
    Calculate the primary region of interest based on motion boxes.

    Args:
        motion_boxes: List of motion detection bounding boxes
        frame_shape: Shape of the video frame (height, width)

    Returns:
        Tuple (x, y, w, h) representing the region of interest center point and dimensions
    """
    # TODO: Implement region of interest calculation
    # 1. Choose a strategy for determining the main area of interest
    #    - You could use the largest motion box
    #    - Or combine nearby boxes
    #    - Or use a weighted average of all motion boxes
    # 2. Return the coordinates of the chosen region

    # Example starter code:
    if not motion_boxes:
        # If no motion is detected, use the center of the frame
        height, width = frame_shape[:2]
        return (width // 2, height // 2, 0, 0)

    # Your implementation here

    total_area = 0
    weighted_x_sum = 0
    weighted_y_sum = 0

    for (x, y, w, h) in motion_boxes:
        area = w * h
        center_x = x + w // 2
        center_y = y + h // 2

        weighted_x_sum += center_x * area
        weighted_y_sum += center_y * area
        total_area += area

    avg_x = int(weighted_x_sum / total_area)
    avg_y = int(weighted_y_sum / total_area)

    return (avg_x, avg_y, 0, 0)


def track_viewport(frames, motion_results, viewport_size, smoothing_factor=0.3):
    """
    Track viewport position across frames with smoothing.

    Args:
        frames: List of video frames
        motion_results: List of motion detection results for each frame
        viewport_size: Tuple (width, height) of the viewport
        smoothing_factor: Factor for smoothing viewport movement (0-1)
                          Lower values create smoother movement

    Returns:
        List of viewport positions for each frame as (x, y) center coordinates
    """
    # TODO: Implement viewport tracking with smoothing
    # 1. For each frame, determine the region of interest based on motion_results
    # 2. Apply smoothing to avoid jerky movements
    #    - Use previous viewport positions to smooth the movement
    #    - Consider implementing a simple exponential moving average
    #    - Or a more advanced approach like Kalman filtering
    # 3. Ensure the viewport stays within the frame boundaries
    # 4. Return the list of viewport positions for all frames

    # Example starter code:
    viewport_positions = []

    # Initialize with center of first frame if available
    if frames:
        height, width = frames[0].shape[:2]
        prev_x, prev_y = width // 2, height // 2
    else:
        return []

    # Your implementation here
    for i in range(len(frames)):
        cx, cy, _, _ = calculate_region_of_interest(motion_results[i], frames[i].shape)

        # Smooth with exponential moving average
        smoothed_x = int(smoothing_factor * cx + (1 - smoothing_factor) * prev_x)
        smoothed_y = int(smoothing_factor * cy + (1 - smoothing_factor) * prev_y)

        # Clip to ensure viewport stays within frame boundaries
        frame_height, frame_width = frames[i].shape[:2]
        half_w, half_h = viewport_size[0] // 2, viewport_size[1] // 2
        smoothed_x = max(half_w, min(frame_width - half_w, smoothed_x))
        smoothed_y = max(half_h, min(frame_height - half_h, smoothed_y))

        viewport_positions.append((smoothed_x, smoothed_y))
        prev_x, prev_y = smoothed_x, smoothed_y

    return viewport_positions

