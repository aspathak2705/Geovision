import cv2
import os

def save_result(results, output_path="outputs/result.jpg"):
    try:
        os.makedirs("outputs", exist_ok=True)

        for r in results:
            annotated = r.plot()  # YOLO draws boxes + labels
            cv2.imwrite(output_path, annotated)

        print(f"[INFO] Output saved at {output_path}")

    except Exception as e:
        print("[ERROR] Visualization failed:", e)