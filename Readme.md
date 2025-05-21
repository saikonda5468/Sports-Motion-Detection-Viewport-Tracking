# 🏀 Sports Motion Detection & Viewport Tracking

This project processes a short sports video to detect motion, track the main area of activity, and simulate a virtual camera that follows the action using **Kalman filtering**. It outputs annotated videos and frames that visualize both motion detection and viewport tracking.

---

## 📦 How to Run

### ✅ Requirements
Install dependencies:
```bash
pip install -r requirements.txt
```

### ✅ Usage

Run the main script with your video file:
```bash
python main.py --video sample_video.mp4 --output output --fps 5 --viewport_size 720x480
```

### Arguments:
| Argument           | Description                             |
|--------------------|-----------------------------------------|
| `--video`          | Path to the input sports video          |
| `--output`         | Output folder to save visualizations    |
| `--fps`            | Frames per second to sample (default: 5)|
| `--viewport_size`  | Viewport size as `WIDTHxHEIGHT` (e.g., 720x480) |

---

## 🧠 System Design & Key Decisions

### 🎥 1. Video Frame Extraction
- **Why**: To analyze a manageable number of frames that capture meaningful movement from the video.
- **How**: Frames are extracted at a target frame rate (e.g., 5 FPS) using OpenCV. Each frame is resized to a consistent resolution for uniform processing.
- **Design Decision**: Downsampling helps reduce computational load while still capturing temporal motion changes accurately.

### 🧠 2. Motion Detection
- **Why**: To identify areas in the frame where significant movement occurs, indicating action in the video.
- **How**:
  - Used frame differencing via `cv2.absdiff()` between the current and previous frames.
  - Applied Gaussian blur to reduce noise before differencing.
  - Applied thresholding and dilation to generate clear motion blobs.
  - Used `cv2.findContours()` to localize movement via bounding boxes.
- **Design Decision**: This simple method balances speed and reliability, making it suitable for short sports clips with frequent movement.

### 🎯 3. Region of Interest (ROI) Estimation
- **Why**: To focus on the center of activity in the frame.
- **How**: Calculated a weighted average of bounding box centers, weighted by the area of each box.
- **Design Decision**: Using area-weighting ensures that larger movement regions (e.g., a group of players) influence the camera focus more than noise or small movement.

### 📍 4. Viewport Tracking with Kalman Filter
- **Why**: To track the center of activity with smooth transitions and predictive ability.
- **How**:
  - Implemented a 2D Kalman filter tracking `[x, y, dx, dy]` (position and velocity).
  - The Kalman filter predicts the next position and corrects it using the detected motion center.
- **Design Decision**: Replacing Exponential Moving Average (EMA) with a Kalman filter improves robustness against erratic or missing measurements and adds motion prediction.

### 🖼️ 5. Visualization
- **Why**: To provide visual feedback on how well the system detects and tracks motion.
- **How**:
  - Overlaid motion bounding boxes in green.
  - Drew a blue rectangle representing the tracked viewport.
  - Saved two video outputs: one with overlays, and one cropped to the viewport region.
- **Design Decision**: This dual-output strategy clearly demonstrates both full-frame processing and the virtual camera effect.

---

## ⚠️ Challenges Encountered

| Challenge                             | Solution Implemented                                            |
|--------------------------------------|------------------------------------------------------------------|
| Jittery viewport motion              | Replaced EMA with Kalman filtering for predictive smoothing     |
| Handling multiple motion regions     | Used area-weighted centroid averaging to find dominant region   |
| Clipping viewport at edges           | Applied boundary checks when computing viewport positions       |
| Visualization cropping errors        | Used top-left/bottom-right bounds carefully to avoid out-of-bounds issues |

---

## 🚀 Ideas for Future Improvements

- 🔄 **Dynamic viewport resizing** based on motion spread
- 🧠 **Player tracking or ball detection** for more targeted focus
- 📉 **Motion heatmaps** to visualize activity distribution
- 🛰️ **Multi-object Kalman tracking** for more robust sports analytics
- ⚙️ **GUI or Streamlit interface** for video upload and parameter tuning

---

## 📁 Output Structure

```
output/
├── motion_detection.mp4        # Full video with overlays
├── viewport_tracking.mp4       # Cropped viewport following action
├── frames/                     # Annotated full frames as images
└── viewport/                   # Cropped viewport frames as images
```
