import cv2
import numpy as np
import os

def detect_change(img1_path, img2_path, output_path="outputs/change.jpg"):
    os.makedirs("outputs", exist_ok=True)

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        print("[ERROR] Could not load images")
        return None

    # Resize
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # ✅ Moderate blur (not too strong)
    gray1 = cv2.GaussianBlur(gray1, (5, 5), 0)
    gray2 = cv2.GaussianBlur(gray2, (5, 5), 0)

    # Difference
    diff = cv2.absdiff(gray1, gray2)

    # Save debug
    cv2.imwrite("outputs/diff.jpg", diff)

    # alanced threshold
    _, thresh = cv2.threshold(diff, 35, 255, cv2.THRESH_BINARY)

    # Morphology
    kernel = np.ones((5, 5), np.uint8)
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    clean = cv2.morphologyEx(clean, cv2.MORPH_CLOSE, kernel)

    # Remove small regions
    contours, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros_like(clean)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 300:   # tuned value
            cv2.drawContours(mask, [cnt], -1, 255, -1)

    cv2.imwrite(output_path, mask)

    print(f"[INFO] Change map saved at {output_path}")

    return mask