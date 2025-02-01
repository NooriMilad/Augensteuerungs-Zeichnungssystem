import cv2
from PIL import Image, ImageDraw
import numpy as np

def draw_rectangle_on_frame(frame, top_left, bottom_right, color, width):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    for i in range(width):
        draw.rectangle([top_left, bottom_right], outline=color)
        top_left = (top_left[0] + 1, top_left[1] + 1)
        bottom_right = (bottom_right[0] - 1, bottom_right[1] - 1)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    top_left = (50, 50)
    bottom_right = (200, 200)
    color = 'red'
    width = 5

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        frame_with_rectangle = draw_rectangle_on_frame(frame, top_left, bottom_right, color, width)
        cv2.imshow('Webcam Feed', frame_with_rectangle)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
