import os
from core.detect import Detector
from core.change import detect_change
from utils.visualize import save_result

T1 = "data/t1/before.png"
T2 = "data/t2/after.png"

OUTPUT_DETECT = "outputs/detect.jpg"
OUTPUT_CHANGE = "outputs/change.jpg"

def main():
    os.makedirs("outputs", exist_ok=True)

    # 1. YOLO Detection (t2)
    detector = Detector()
    results = detector.run(T2)
    save_result(results, OUTPUT_DETECT)

    # 2. Change Detection
    detect_change(T1, T2, OUTPUT_CHANGE)

    

if __name__ == "__main__":
    main()