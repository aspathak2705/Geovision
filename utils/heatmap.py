import cv2
import numpy as np

def generate_heatmap(image_path, change_boxes, output_path):
    img = cv2.imread(image_path)
    heatmap = np.zeros((img.shape[0], img.shape[1]), dtype=np.float32)

    for (x1, y1, x2, y2) in change_boxes:
        heatmap[y1:y2, x1:x2] += 1

    # Normalize
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)

    heatmap = heatmap.astype(np.uint8)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)

    cv2.imwrite(output_path, overlay)