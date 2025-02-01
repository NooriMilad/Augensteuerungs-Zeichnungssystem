import cv2
from PIL import Image, ImageDraw
import numpy as np

class DrawingTools:
    def __init__(self):
        self.pen_color = (0, 0, 0)  # Default pen color is black
        self.top_left = (0, 0)
        self.bottom_right = (0, 0)
        self.color = (255, 0, 0)  # Default rectangle color is red
        self.width = 1  # Default rectangle border width

    def set_pen_color(self, color):
        self.pen_color = color

    def draw_rectangle_on_frame(self, frame):
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        top_left = self.top_left
        bottom_right = self.bottom_right
        for i in range(self.width):
            draw.rectangle([top_left, bottom_right], outline=self.color)
            top_left = (top_left[0] + 1, top_left[1] + 1)
            bottom_right = (bottom_right[0] - 1, bottom_right[1] - 1)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def set_rectangle_params(self, top_left, bottom_right, color, width):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.color = color
        self.width = width

    def update_rectangle_position(self, gaze_coordinates):
        # Update the rectangle position based on gaze coordinates
        x, y = gaze_coordinates
        self.top_left = (x - 75, y - 75)
        self.bottom_right = (x + 75, y + 75)

    # Add your drawing methods here