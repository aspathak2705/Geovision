import json
from pathlib import Path

import cv2

from core.detect import Detector
from core.fusion import analyze_changes, draw_fusion
from utils.heatmap import generate_heatmap
from utils.visualize import save_result


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_T1_PATH = PROJECT_ROOT / "data" / "t1" / "before.png"
DEFAULT_T2_PATH = PROJECT_ROOT / "data" / "t2" / "after.png"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
METRICS_PATH = OUTPUT_DIR / "metrics.json"


def _relative(path):
    return str(Path(path).resolve().relative_to(PROJECT_ROOT))


def _fit_to_canvas(image, target_height, target_width):
    src_height, src_width = image.shape[:2]
    scale = min(target_width / src_width, target_height / src_height)
    resized_width = max(1, int(round(src_width * scale)))
    resized_height = max(1, int(round(src_height * scale)))
    resized = cv2.resize(image, (resized_width, resized_height), interpolation=cv2.INTER_LINEAR)

    canvas = cv2.copyMakeBorder(
        resized,
        (target_height - resized_height) // 2,
        target_height - resized_height - (target_height - resized_height) // 2,
        (target_width - resized_width) // 2,
        target_width - resized_width - (target_width - resized_width) // 2,
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0),
    )
    return canvas


def normalize_pair(img1_path, img2_path, output_path=None):
    img1_path = Path(img1_path)
    img2_path = Path(img2_path)
    output_path = Path(output_path or PROJECT_ROOT / "data" / "t2" / "normalized.jpg")

    img1 = cv2.imread(str(img1_path))
    img2 = cv2.imread(str(img2_path))

    if img1 is None:
        raise FileNotFoundError(f"Could not read baseline image: {img1_path}")
    if img2 is None:
        raise FileNotFoundError(f"Could not read comparison image: {img2_path}")

    h, w = img1.shape[:2]
    if img2.shape[:2] != (h, w):
        img2 = _fit_to_canvas(img2, h, w)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), img2)

    return img1_path, output_path


def run_analysis(
    t1_path=DEFAULT_T1_PATH,
    t2_path=DEFAULT_T2_PATH,
    confidence=0.6,
    iou_threshold=0.3,
):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    t1_path, t2_path = normalize_pair(t1_path, t2_path)
    detector = Detector(confidence=confidence)

    boxes_t1, res1 = detector.run(str(t1_path))
    boxes_t2, res2 = detector.run(str(t2_path))

    detect_t1_path = OUTPUT_DIR / "detect_t1.jpg"
    detect_t2_path = OUTPUT_DIR / "detect_t2.jpg"
    fusion_path = OUTPUT_DIR / "fusion.jpg"
    heatmap_path = OUTPUT_DIR / "heatmap.jpg"

    save_result([res1], str(detect_t1_path))
    save_result([res2], str(detect_t2_path))

    new, removed, unchanged = analyze_changes(boxes_t1, boxes_t2, iou_thresh=iou_threshold)
    draw_fusion(str(t2_path), new, removed, unchanged, str(fusion_path))
    generate_heatmap(str(t2_path), new + removed, str(heatmap_path))

    total = len(new) + len(removed) + len(unchanged)
    changed = len(new) + len(removed)
    change_percent = (changed / total * 100) if total else 0

    metrics = {
        "new": len(new),
        "removed": len(removed),
        "unchanged": len(unchanged),
        "total": total,
        "changed": changed,
        "change_percent": round(change_percent, 2),
        "confidence": confidence,
        "iou_threshold": iou_threshold,
        "paths": {
            "t1": _relative(t1_path),
            "t2": _relative(t2_path),
            "detect_t1": _relative(detect_t1_path),
            "detect_t2": _relative(detect_t2_path),
            "fusion": _relative(fusion_path),
            "heatmap": _relative(heatmap_path),
        },
    }

    with METRICS_PATH.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return metrics


def load_metrics():
    if not METRICS_PATH.exists():
        return None
    with METRICS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
