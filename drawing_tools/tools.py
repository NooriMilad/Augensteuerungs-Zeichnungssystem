import cv2
from PIL import Image, ImageDraw
import numpy as np

class DrawingTools:
    def __init__(self):
        self.pen_color = (0, 0, 0)  # Default pen color is black
        self.stroke_width = 1  # Default stroke width
        self.tool = 'brush'  # Default tool
        self.top_left = (0, 0)
        self.bottom_right = (0, 0)
        self.color = (255, 0, 0)  # Default rectangle color is red
        self.width = 1  # Default rectangle border width

    def set_pen_color(self, color):
        self.pen_color = color

    def set_stroke_width(self, width):
        self.stroke_width = width

    def set_tool(self, tool):
        self.tool = tool

    def draw_on_frame(self, frame, gaze_coordinates):
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        x, y = gaze_coordinates

        if self.tool == 'brush':
            draw.ellipse((x - self.stroke_width, y - self.stroke_width, x + self.stroke_width, y + self.stroke_width), fill=self.pen_color)
        elif self.tool == 'shape':
            draw.rectangle([self.top_left, self.bottom_right], outline=self.color, width=self.width)
        elif self.tool == 'fill':
            draw.rectangle([0, 0, img.width, img.height], fill=self.pen_color)
        elif self.tool == 'airbrush':
            for _ in range(10):  # Simulate airbrush effect
                offset_x = np.random.randint(-self.stroke_width, self.stroke_width)
                offset_y = np.random.randint(-self.stroke_width, self.stroke_width)
                draw.point((x + offset_x, y + offset_y), fill=self.pen_color)

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