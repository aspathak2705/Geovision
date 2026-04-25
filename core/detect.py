from ultralytics import YOLO

class Detector:
    def __init__(self, model_path="models/yolo_building.pt", confidence=0.6):
        self.model = YOLO(model_path)
        self.confidence = confidence

    def run(self, image_path):
        results = self.model(image_path, conf=self.confidence)[0]

        boxes = []

        for box in results.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)

            # Filter small boxes
            area = (x2 - x1) * (y2 - y1)
            if area > 500:   # adjust if needed
                boxes.append([x1, y1, x2, y2])

        return boxes, results
