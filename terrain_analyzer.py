import cv2
import numpy as np


def analyze_lunar_terrain(image):
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    edges = cv2.Canny(blur, 50, 150)

    output = image.copy()
    danger_mask = np.zeros(gray.shape, dtype=np.uint8)

    # Hough Circle crater detection
    circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=35,
        param1=80,
        param2=28,
        minRadius=8,
        maxRadius=90
    )

    crater_count = 0

    if circles is not None:
        circles = np.uint16(np.around(circles))
        crater_count = len(circles[0])

        for circle in circles[0, :]:
            x, y, r = circle
            cv2.circle(output, (x, y), r, (0, 0, 255), 2)
            cv2.circle(danger_mask, (x, y), r + 20, 255, -1)

    # Contour-based rough terrain detection
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rough_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 120:
            rough_area += area
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(danger_mask, (x, y), (x + w, y + h), 255, -1)

    total_area = gray.shape[0] * gray.shape[1]
    danger_area = np.count_nonzero(danger_mask)
    safe_area = total_area - danger_area

    safe_percentage = round((safe_area / total_area) * 100, 2)
    roughness_score = round((rough_area / total_area) * 100, 2)

    risk_score = int(
        min(
            100,
            (crater_count * 8) + (roughness_score * 2) + ((100 - safe_percentage) * 0.7)
        )
    )

    safe_mask = cv2.bitwise_not(danger_mask)

    safe_contours, _ = cv2.findContours(
        safe_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    recommended_coordinates = None
    largest_safe_area = 0

    for contour in safe_contours:
        area = cv2.contourArea(contour)

        if area > 2500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                output,
                "SAFE ZONE",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            if area > largest_safe_area:
                largest_safe_area = area
                recommended_coordinates = (x + w // 2, y + h // 2)

    if recommended_coordinates:
        cx, cy = recommended_coordinates
        cv2.circle(output, (cx, cy), 8, (255, 255, 0), -1)
        cv2.putText(
            output,
            "LAND HERE",
            (cx + 10, cy),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )

    # Heatmap
    heatmap = cv2.applyColorMap(danger_mask, cv2.COLORMAP_JET)
    heatmap = cv2.addWeighted(image, 0.6, heatmap, 0.4, 0)

    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    dashboard = {
        "crater_count": crater_count,
        "safe_area_percentage": safe_percentage,
        "terrain_roughness_score": roughness_score,
        "risk_score": risk_score,
        "recommended_coordinates": recommended_coordinates
    }

    return output, edges, heatmap, dashboard