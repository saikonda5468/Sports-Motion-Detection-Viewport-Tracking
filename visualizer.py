"""
Visualization functions for displaying motion detection and viewport tracking results.
"""

import os
import cv2
import numpy as np

def visualize_results(
    frames, motion_results, viewport_positions, viewport_size, output_dir
):
    """
    Create visualization of motion detection and viewport tracking results.

    Args:
        frames: List of video frames
        motion_results: List of motion detection results for each frame
        viewport_positions: List of viewport center positions for each frame
        viewport_size: Tuple (width, height) of the viewport
        output_dir: Directory to save visualization results
    """
    # Create directories to save annotated full frames and cropped viewports
    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    viewport_dir = os.path.join(output_dir, "viewport")
    os.makedirs(viewport_dir, exist_ok=True)

    # Get original frame dimensions
    height, width = frames[0].shape[:2]

    # Create video writer for full annotated frame video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_path = os.path.join(output_dir, "motion_detection.mp4")
    video_writer = cv2.VideoWriter(video_path, fourcc, 5, (width, height))

    # Create video writer for cropped viewport-only video
    viewport_video_path = os.path.join(output_dir, "viewport_tracking.mp4")
    vp_width, vp_height = viewport_size
    viewport_writer = cv2.VideoWriter(
        viewport_video_path, fourcc, 5, (vp_width, vp_height)
    )

    # Loop over each frame to annotate and extract viewport
    for i, frame in enumerate(frames):
        vis_frame = frame.copy()  # Work on a copy to preserve the original

        # Draw green motion detection bounding boxes
        for (x, y, w, h) in motion_results[i]:
            cv2.rectangle(vis_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw blue viewport rectangle centered at predicted location
        cx, cy = viewport_positions[i]
        half_w, half_h = vp_width // 2, vp_height // 2
        top_left = (cx - half_w, cy - half_h)
        bottom_right = (cx + half_w, cy + half_h)
        cv2.rectangle(vis_frame, top_left, bottom_right, (255, 0, 0), 2)

        # Extract the viewport area from the frame
        crop = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # Overlay frame number as yellow text
        cv2.putText(vis_frame, f"Frame {i+1}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Save the annotated frame and cropped viewport as images
        cv2.imwrite(os.path.join(frames_dir, f"frame_{i:03d}.jpg"), vis_frame)
        cv2.imwrite(os.path.join(viewport_dir, f"viewport_{i:03d}.jpg"), crop)

        # Add frames to the corresponding output videos
        video_writer.write(vis_frame)
        viewport_writer.write(crop)

    # Release the video writers
    video_writer.release()
    viewport_writer.release()

    # Print output paths for confirmation
    print(f"Visualization saved to {video_path}")
    print(f"Viewport video saved to {viewport_video_path}")
    print(f"Individual frames saved to {frames_dir} and {viewport_dir}")
