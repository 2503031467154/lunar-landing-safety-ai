import cv2
import numpy as np

def analyze_lunar_terrain(image):
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    edges = cv2.Canny(blur, 50, 150)

    circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=40,
        param1=80,
        param2=30,
        minRadius=10,
        maxRadius=80
    )

    output = image.copy()
    danger_mask = np.zeros(gray.shape, dtype=np.uint8)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, r = circle
            cv2.circle(output, (x, y), r, (0, 0, 255), 2)
            cv2.circle(danger_mask, (x, y), r + 20, 255, -1)

    safe_mask = cv2.bitwise_not(danger_mask)

    contours, _ = cv2.findContours(
        safe_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 3000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(output, "SAFE ZONE", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

    return output, edges