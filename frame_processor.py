"""
Frame processing functions for the motion detection project.
"""

import cv2
import numpy as np


def process_video(video_path, target_fps=5, resize_dim=(1280, 720)):
    """
    Extract frames from a video at a specified frame rate.

    Args:
        video_path: Path to the video file
        target_fps: Target frames per second to extract
        resize_dim: Dimensions to resize frames to (width, height)

    Returns:
        List of extracted frames
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    # Get video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate frame interval for the target FPS
    frame_interval = max(1, int(original_fps / target_fps))

    # TODO: Implement frame extraction
    # 1. Read frames from the video capture object
    # 2. Only keep frames at the specified interval to achieve target_fps
    # 3. Resize frames to the specified dimensions
    # 4. Store frames in a list
    # 5. Release the video capture object when done
    

    # Example starter code:
    frames = []
    frame_index = 0

    # Your implementation here
        # Loop through the video frame by frame
    while cap.isOpened():
        # Read a single frame from the video
        ret, frame = cap.read()

        # Break the loop if no frame is returned (end of video)
        if not ret:
            break

        # Process and store the frame only at specified intervals to match target FPS
        if frame_index % frame_interval == 0:
            # Resize the frame to the desired dimensions (e.g., 1280x720)
            resized_frame = cv2.resize(frame, resize_dim)
            # Append the resized frame to the list
            frames.append(resized_frame)

        # Move to the next frame
        frame_index += 1

    # Release the video capture object to free resources
    cap.release()

    # Return the list of extracted and resized frames

    return frames
