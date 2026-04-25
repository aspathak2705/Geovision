import os
import cv2
from core.detect import Detector
from core.fusion import analyze_changes, draw_fusion
from utils.visualize import save_result
from utils.heatmap import generate_heatmap

T1_PATH = "data/t1/before.png"
T2_PATH = "data/t2/after.png"


#Resize Images
def resize_pair(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        print("[ERROR] Failed to load images")
        return None, None

    h, w = img1.shape[:2]
    img2_resized = cv2.resize(img2, (w, h))

    resized_path = "data/t2/resized.jpg"
    cv2.imwrite(resized_path, img2_resized)

    return img1_path, resized_path


def main():
    os.makedirs("outputs", exist_ok=True)

    # 1. Resize images
    T1, T2 = resize_pair(T1_PATH, T2_PATH)

    if T1 is None:
        return

    # 2. Load detector
    detector = Detector()

    # 3. Run detection
    boxes_t1, res1 = detector.run(T1)
    boxes_t2, res2 = detector.run(T2)

    # Save clean detection visuals
    save_result([res1], "outputs/detect_t1.jpg")
    save_result([res2], "outputs/detect_t2.jpg")

    # 4. Fusion (IoU-based)
    new, removed, unchanged = analyze_changes(boxes_t1, boxes_t2)

    # Save fusion result
    draw_fusion(T2, new, removed, unchanged, "outputs/fusion.jpg")

    print(f"[INFO] New: {len(new)}")
    print(f"[INFO] Removed: {len(removed)}")
    print(f"[INFO] Unchanged: {len(unchanged)}")

    # 5. Heatmap Generation 
    change_boxes = new + removed
    generate_heatmap(T2, change_boxes, "outputs/heatmap.jpg")



if __name__ == "__main__":
    main()