import cv2
import math

def compute_iou(box1, box2):
    x1, y1, x2, y2 = box1
    x1_p, y1_p, x2_p, y2_p = box2

    xi1 = max(x1, x1_p)
    yi1 = max(y1, y1_p)
    xi2 = min(x2, x2_p)
    yi2 = min(y2, y2_p)

    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2_p - x1_p) * (y2_p - y1_p)

    union = box1_area + box2_area - inter_area

    return inter_area / union if union != 0 else 0


def analyze_changes(boxes_t1, boxes_t2, iou_thresh=0.3):
    matched_t2 = set()

    removed = []
    unchanged = []
    new = []

    # Check t1 → removed / unchanged
    for i, b1 in enumerate(boxes_t1):
        found = False

        for j, b2 in enumerate(boxes_t2):
            if(compute_iou(b1, b2) > iou_thresh) or (centroid_distance(b1, b2) < 30):
                found = True
                matched_t2.add(j)
                unchanged.append(b2)
                break

        if not found:
            removed.append(b1)

    # Check t2 → new
    for j, b2 in enumerate(boxes_t2):
        if j not in matched_t2:
            new.append(b2)

    return new, removed, unchanged


def draw_fusion(image_path, new, removed, unchanged, output_path):
    img = cv2.imread(image_path)

    # New → Green
    for (x1, y1, x2, y2) in new:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)

    # Removed → Red
    for (x1, y1, x2, y2) in removed:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)

    # Unchanged → Blue
    for (x1, y1, x2, y2) in unchanged:
        cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 1)

    cv2.imwrite(output_path, img)


def centroid(box):
    x1, y1, x2, y2 = box
    return ((x1 + x2) // 2, (y1 + y2) // 2)

def centroid_distance(box1, box2):
    c1 = centroid(box1)
    c2 = centroid(box2)
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)