import cv2
import numpy as np

def generate_heatmap(image_path, change_boxes, output_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image for heatmap: {image_path}")

    if not change_boxes:
        cv2.imwrite(output_path, img)
        return

    heatmap = np.zeros((img.shape[0], img.shape[1]), dtype=np.float32)

    for (x1, y1, x2, y2) in change_boxes:
        heatmap[y1:y2, x1:x2] += 1

    normalized = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    colored = cv2.applyColorMap(normalized, cv2.COLORMAP_JET)

    overlay = img.copy()
    active_mask = normalized > 0
    overlay[active_mask] = cv2.addWeighted(
        img[active_mask],
        0.55,
        colored[active_mask],
        0.45,
        0,
    )

    cv2.imwrite(output_path, overlay)
