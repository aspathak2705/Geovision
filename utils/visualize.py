import cv2
import os

def save_result(results, output_path="outputs/result.jpg"):
    os.makedirs("outputs", exist_ok=True)

    for r in results:
        img = r.orig_img.copy()

        # Draw only bounding boxes (clean view)
        for box in r.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

        cv2.imwrite(output_path, img)

    print(f"[INFO] Saved: {output_path}")