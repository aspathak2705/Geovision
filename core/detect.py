from ultralytics import YOLO

class Detector:
    def __init__(self, model_path="models/yolo_building.pt"):
        try:
            self.model = YOLO(model_path)
            print(f"[INFO] Model loaded from {model_path}")
        except Exception as e:
            print("[ERROR] Failed to load model:", e)

    def run(self, image_path):
        try:
            results = self.model(image_path)
            print(f"[INFO] Detection completed on {image_path}")
            return results
        except Exception as e:
            print("[ERROR] Detection failed:", e)
            return None