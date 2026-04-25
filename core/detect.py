from ultralytics import YOLO

class Detector:
    def __init__(self, model_path="models/yolo_building.pt"):
        self.model = YOLO(model_path)

    def run(self, image_path):
        # Increase confidence threshold
        results = self.model(image_path, conf=0.6)[0]

        boxes = []

        for box in results.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)

            # Filter small boxes
            area = (x2 - x1) * (y2 - y1)
            if area > 500:   # adjust if needed
                boxes.append([x1, y1, x2, y2])

        return boxes, results