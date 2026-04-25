<div align="center">
  <img src="https://img.icons8.com/color/96/000000/satellite.png" alt="GeoVision Logo" width="80" />
  <h1 align="center">GeoVision</h1>
  <p align="center">
    <strong>An object-centric satellite change detection system for building-level geospatial intelligence</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Interface-Streamlit-FF4B4B" alt="Streamlit" />
    <img src="https://img.shields.io/badge/Detection-YOLOv8-111827" alt="YOLOv8" />
    <img src="https://img.shields.io/badge/Vision-OpenCV-5C3EE8" alt="OpenCV" />
    <img src="https://img.shields.io/badge/Language-Python-3776AB" alt="Python" />
  </p>
  <a href="https://geovision-aig8.onrender.com">Deployment Link</a>
</div>

---

## Overview

**GeoVision** is a satellite change analytics project that detects and explains building-level changes between two temporal satellite images.

Instead of relying on fragile pixel-by-pixel comparison, GeoVision uses an **object-centric pipeline**:

- detect buildings in the `t1` baseline image
- detect buildings in the `t2` comparison image
- match detected objects using spatial reasoning
- classify buildings as **new**, **removed**, or **unchanged**
- generate visual outputs for detection, fusion, heatmap density, and summary metrics
- present results through a professional Streamlit dashboard

The system is designed for real-world satellite imagery where images may contain small spatial shifts, different lighting, seasonal changes, resolution variation, and map overlays.

<br>

## Key Features

- **User-driven dashboard workflow:** Users upload the two satellite images, run analysis, and then inspect generated outputs.
- **YOLO-based building detection:** Uses a trained YOLO model stored at `models/yolo_building.pt`.
- **Object-centric change detection:** Compares detected building objects instead of raw pixels.
- **Hybrid spatial matching:** Combines IoU, centroid distance, and neighbor-aware matching.
- **Change classification:** Separates objects into new, removed, and unchanged categories.
- **Fusion visualization:** Draws semantic change overlays on the comparison image.
- **Change density heatmap:** Highlights regions with high concentrations of new or removed objects.
- **Analytics dashboard:** Displays counts, change percentage, class distribution, and generated insights.
- **CLI and dashboard entrypoints:** Supports both `python run.py` and `streamlit run app/main.py`.

<br>

## Real-World Challenge

Satellite-based change detection traditionally relies on pixel-level methods such as image differencing, thresholding, or segmentation models like U-Net.

During development, a major real-world issue appeared:

> Satellite images captured at different times are often not perfectly aligned and can vary in lighting, resolution, perspective, shadows, overlays, and seasonal vegetation.

This can cause pixel-based approaches to fail because small differences may be incorrectly interpreted as structural change.

Common failure cases include:

- false positives from 2 to 5 pixel spatial shifts
- large regions being incorrectly marked as changed
- sensitivity to shadows and illumination differences
- vegetation or seasonal changes being confused with construction changes
- map labels or overlay text affecting pixel comparison
- perspective and resolution differences between image captures

The key insight behind GeoVision is:

> In real-world geospatial systems, object-level reasoning combined with spatial context is more reliable than pixel-level comparison alone.

<br>

## Proposed Solution: Object-Centric Change Detection

GeoVision solves the above issue by comparing detected objects rather than comparing raw pixels.

### Step 1: Object Detection

YOLO is applied independently to both images:

```text
t1 image -> buildings_t1
t2 image -> buildings_t2
```

Each detected building is represented as a bounding box.

### Step 2: Multi-Level Object Matching

Because buildings do not have persistent IDs across images, GeoVision uses a hybrid spatial matching strategy.

#### 1. IoU Matching

Bounding boxes are compared using Intersection over Union.

```text
If IoU > threshold -> same object
```

#### 2. Centroid Distance Matching

To handle small misalignments, object centers are compared.

```text
If centroid distance is small -> likely same object
```

#### 3. Neighbor-Aware Matching

For dense urban regions, GeoVision also compares nearby object context.

Each building is interpreted relative to surrounding structures using:

- nearby building positions
- spatial layout consistency
- neighborhood pattern similarity

This improves robustness when bounding boxes shift slightly between images.

### Step 3: Change Classification

| Condition | Classification |
|----------|----------------|
| Object appears in `t2` but not in `t1` | New building |
| Object appears in `t1` but not in `t2` | Removed building |
| Object matches across both images | Unchanged building |

### Step 4: Heatmap-Based Change Density

GeoVision combines all new and removed object regions to produce a heatmap layer.

The heatmap helps identify:

- high-activity development zones
- demolition or removal clusters
- spatial concentration of structural changes
- macro-level urban transformation patterns

<br>

## Architecture & Tech Stack

GeoVision is organized into a computer vision pipeline and a Streamlit dashboard.

### Computer Vision Pipeline

- **Model Runtime:** Ultralytics YOLO
- **Image Processing:** OpenCV
- **Numerical Processing:** NumPy
- **Detection Target:** Buildings
- **Model File:** `models/yolo_building.pt`

### Dashboard

- **Framework:** Streamlit
- **Pages:**
  - Upload
  - Results
  - Analytics
  - About / Methodology
- **Design Style:** Light-mode institutional dashboard with clinical cards, emerald status states, slate navigation, and compact analysis panels

### Output Artifacts

Each analysis run generates:

| File | Description |
|------|-------------|
| `outputs/detect_t1.jpg` | Detection overlay for the baseline image |
| `outputs/detect_t2.jpg` | Detection overlay for the comparison image |
| `outputs/fusion.jpg` | Semantic fusion output with new, removed, and unchanged objects |
| `outputs/heatmap.jpg` | Change density heatmap |
| `outputs/metrics.json` | Generated metrics and output paths |

<br>

## Product Modules

### Upload

Users upload:

- `t1`: baseline satellite image
- `t2`: comparison satellite image

The dashboard requires both images before running analysis. It does not display predefined results as user-facing output.

### Results

Displays generated analysis outputs after a successful run:

- t1 detection cluster
- t2 detection cluster
- temporal fusion output
- change density heatmap

### Analytics

Summarizes:

- total detected objects
- new objects
- removed objects
- unchanged objects
- change percentage
- class distribution
- basic intelligence insights

### About / Methodology

Documents the system workflow:

1. input alignment
2. YOLO detection
3. spatial matching
4. fusion output
5. heatmap synthesis
6. metrics export

<br>

## Project Structure

```text
GeoVision/
|-- app/                         # Streamlit dashboard
|   |-- main.py                   # Dashboard entrypoint
|   |-- pages/
|   |   |-- 1_Upload.py           # User image upload and analysis trigger
|   |   |-- 2_Results.py          # Generated visual outputs
|   |   |-- 3_Analytics.py        # Metrics and insights
|   |   |-- 4_About.py            # Methodology page
|   |-- components/
|       |-- uploader.py           # Upload helpers
|       |-- image_viewer.py       # Result image presentation
|       |-- metrics_panel.py      # Shared design system and metric cards
|       |-- heatmap_view.py       # Heatmap display component
|-- core/
|   |-- detect.py                 # YOLO building detector wrapper
|   |-- fusion.py                 # IoU, centroid, neighbor matching, fusion drawing
|   |-- pipeline.py               # End-to-end reusable analysis pipeline
|-- utils/
|   |-- visualize.py              # Detection image writer
|   |-- heatmap.py                # Heatmap generation
|-- data/
|   |-- t1/                       # Internal storage for uploaded baseline image
|   |-- t2/                       # Internal storage for uploaded comparison image
|-- models/
|   |-- yolo_building.pt          # Trained YOLO building detection model
|-- outputs/                      # Generated analysis outputs
|-- Dashboard/
|   |-- app.py                    # Compatibility wrapper for app/main.py
|-- Custom_yolo_trainig.ipynb     # Model training notebook
|-- run.py                        # CLI entrypoint
|-- requirements.txt
|-- README.md
```

<br>

## Getting Started

### Prerequisites

- Python `3.10+` recommended
- `pip`
- A trained YOLO model at:

```text
models/yolo_building.pt
```

### 1. Install Dependencies

From the project root:

```bash
pip install -r requirements.txt
```

The core dependencies are:

```text
ultralytics
opencv-python
numpy
streamlit
```

### 2. Run the Dashboard

```bash
streamlit run app/main.py
```

Default local URL:

```text
http://localhost:8501
```

If Streamlit starts on another port, use the URL shown in the terminal.

### 3. Use the Dashboard

1. Open the Upload page.
2. Upload the baseline satellite image (`t1`).
3. Upload the comparison satellite image (`t2`).
4. Adjust confidence and matching sensitivity if needed.
5. Click **Run Analysis**.
6. Open Results and Analytics to inspect generated output.

<br>

## CLI Usage

GeoVision can also be run without the dashboard:

```bash
python run.py
```

The CLI uses:

```text
data/t1/before.png
data/t2/after.png
```

and writes results to:

```text
outputs/
```

<br>

## Configuration

### Detection Confidence

The detector accepts a confidence threshold:

```python
Detector(confidence=0.6)
```

In the dashboard this is controlled by the **Confidence threshold** slider.

### Matching Sensitivity

The fusion step accepts an IoU threshold:

```python
analyze_changes(boxes_t1, boxes_t2, iou_thresh=0.3)
```

In the dashboard this is controlled by the **Matching sensitivity** slider.

<br>

## Methodology Details

### Detection

`core/detect.py` loads `models/yolo_building.pt` through Ultralytics YOLO and extracts bounding boxes.

Small detections are filtered using a minimum area threshold to reduce noise:

```text
area > 500 pixels
```

### Fusion

`core/fusion.py` classifies detections using:

- IoU overlap
- centroid distance
- neighbor similarity

The current matching logic treats a pair of objects as the same if any of the following is true:

```text
IoU > threshold
centroid distance < 30 pixels
neighbor similarity >= 2
```

### Heatmap

`utils/heatmap.py` accumulates spatial frequency over all changed boxes and overlays the normalized heatmap on the comparison image.

<br>

## Why This Approach Works Better

GeoVision is more robust than direct pixel comparison because it:

- does not require pixel-perfect alignment
- reduces false changes caused by lighting and shadows
- produces object-level explanations
- supports dense urban matching through neighborhood context
- adds heatmap-level interpretation for non-technical users

The result is an interpretable workflow:

```text
New construction detected
Building removed
Unchanged structure retained
High activity zone identified
```

<br>

## Current Limitations

- Accuracy depends on the quality of the YOLO building detector.
- Missed detections can create false new or removed classifications.
- Dense urban areas can still create ambiguous object matches.
- The current resizing step aligns image dimensions but does not perform full georectification.
- Map labels, text overlays, and very different viewpoints may still affect detection quality.
- Output files in `outputs/` are overwritten on each analysis run.

<br>

## Future Improvements

- add geospatial registration before detection
- support GeoTIFF metadata and coordinate-aware outputs
- add confidence scores per changed object
- export reports as PDF
- add side-by-side before/after comparison controls
- store analysis history instead of overwriting outputs
- add automated tests for detection, fusion, and dashboard flows
- support multiple object classes beyond buildings

<br>

## Resume Highlight

Developed an object-centric satellite change detection system using YOLO and spatial-context matching, augmented with heatmap-based change density analysis to overcome alignment and noise limitations of traditional pixel-based methods.

---

<div align="center">
  <p>Built for interpretable satellite monitoring, urban change analytics, and real-world geospatial intelligence.</p>
</div>
