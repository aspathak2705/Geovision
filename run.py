import os
import cv2
from core.detect import Detector
from core.fusion import analyze_changes, draw_fusion
from utils.visualize import save_result
from utils.heatmap import generate_heatmap

T1_PATH = "data/t1/before.png"
T2_PATH = "data/t2/after.png"


def resize_pair(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    h, w = img1.shape[:2]
    img2 = cv2.resize(img2, (w, h))

    resized_path = "data/t2/resized.jpg"
    cv2.imwrite(resized_path, img2)

    return img1_path, resized_path


def main():
    os.makedirs("outputs", exist_ok=True)

    # Resize
    T1, T2 = resize_pair(T1_PATH, T2_PATH)

    detector = Detector()

    # Detection
    boxes_t1, res1 = detector.run(T1)
    boxes_t2, res2 = detector.run(T2)

    save_result([res1], "outputs/detect_t1.jpg")
    save_result([res2], "outputs/detect_t2.jpg")

    # Fusion
    new, removed, unchanged = analyze_changes(boxes_t1, boxes_t2)

    draw_fusion(T2, new, removed, unchanged, "outputs/fusion.jpg")

    # Heatmap
    generate_heatmap(T2, new + removed, "outputs/heatmap.jpg")

    # Metrics
    total = len(new) + len(removed) + len(unchanged)
    change_percent = ((len(new) + len(removed)) / total * 100) if total > 0 else 0

    print("\n📊 RESULTS")
    print(f"New: {len(new)}")
    print(f"Removed: {len(removed)}")
    print(f"Unchanged: {len(unchanged)}")
    print(f"Change %: {change_percent:.2f}%")

    print("\n✅ System Completed Successfully")


if __name__ == "__main__":
    main()