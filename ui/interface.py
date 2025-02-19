import tkinter as tk
from tkinter import colorchooser, messagebox, ttk
from threading import Thread
import cv2
from PIL import Image, ImageTk

class UserInterface:
    def __init__(self, cursor_controller, drawing_tools, eye_tracker):
        self.cursor_controller = cursor_controller
        self.drawing_tools = drawing_tools
        self.eye_tracker = eye_tracker
        self.root = tk.Tk()
        self.root.title("Eye Tracking Communication System")
        self.root.geometry("1024x768")  # Set the window size
        self.drawing_active = False
        self.pen_color = "black"  # Default pen color

        # Create a main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the camera feed
        self.camera_frame = ttk.Frame(self.main_frame, width=300, height=300)
        self.camera_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        self.camera_frame.pack_propagate(False)

        # Create a canvas for displaying the webcam feed
        self.canvas = tk.Canvas(self.camera_frame, width=300, height=300)
        self.canvas.pack()

        # Create a frame for the drawing tools
        self.tools_frame = ttk.Frame(self.main_frame, width=200)
        self.tools_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Add buttons for drawing tools
        self.brush_button = ttk.Button(self.tools_frame, text="Brush", command=self.set_brush_tool)
        self.brush_button.pack(pady=5)
        self.shape_button = ttk.Button(self.tools_frame, text="Shape", command=self.set_shape_tool)
        self.shape_button.pack(pady=5)
        self.fill_button = ttk.Button(self.tools_frame, text="Fill", command=self.set_fill_tool)
        self.fill_button.pack(pady=5)
        self.airbrush_button = ttk.Button(self.tools_frame, text="Airbrush", command=self.set_airbrush_tool)
        self.airbrush_button.pack(pady=5)

        # Add color picker
        self.color_picker_button = ttk.Button(self.tools_frame, text="Choose Color", command=self.choose_color)
        self.color_picker_button.pack(pady=5)

        # Add stroke width slider
        self.stroke_width_slider = ttk.Scale(self.tools_frame, from_=1, to=10, orient=tk.HORIZONTAL, command=self.set_stroke_width)
        self.stroke_width_slider.pack(pady=5)

        # Add buttons for additional drawing tools
        self.text_button = ttk.Button(self.tools_frame, text="Text", command=self.set_text_tool)
        self.text_button.pack(pady=5)
        self.line_button = ttk.Button(self.tools_frame, text="Line", command=self.set_line_tool)
        self.line_button.pack(pady=5)
        self.curve_button = ttk.Button(self.tools_frame, text="Curve", command=self.set_curve_tool)
        self.curve_button.pack(pady=5)
        self.rectangle_button = ttk.Button(self.tools_frame, text="Rectangle", command=self.set_rectangle_tool)
        self.rectangle_button.pack(pady=5)
        self.polygon_button = ttk.Button(self.tools_frame, text="Polygon", command=self.set_polygon_tool)
        self.polygon_button.pack(pady=5)
        self.ellipse_button = ttk.Button(self.tools_frame, text="Ellipse", command=self.set_ellipse_tool)
        self.ellipse_button.pack(pady=5)
        self.rounded_rectangle_button = ttk.Button(self.tools_frame, text="Rounded Rectangle", command=self.set_rounded_rectangle_tool)
        self.rounded_rectangle_button.pack(pady=5)

        # Start the video feed
        self.video_feed()

    def set_brush_tool(self):
        self.drawing_tools.set_tool('brush')

    def set_shape_tool(self):
        self.drawing_tools.set_tool('shape')

    def set_fill_tool(self):
        self.drawing_tools.set_tool('fill')

    def set_airbrush_tool(self):
        self.drawing_tools.set_tool('airbrush')

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color
            self.drawing_tools.set_pen_color(color)

    def set_stroke_width(self, width):
        self.drawing_tools.set_stroke_width(int(width))

    def set_text_tool(self):
        self.drawing_tools.set_tool('text')

    def set_line_tool(self):
        self.drawing_tools.set_tool('line')

    def set_curve_tool(self):
        self.drawing_tools.set_tool('curve')

    def set_rectangle_tool(self):
        self.drawing_tools.set_tool('rectangle')

    def set_polygon_tool(self):
        self.drawing_tools.set_tool('polygon')

    def set_ellipse_tool(self):
        self.drawing_tools.set_tool('ellipse')

    def set_rounded_rectangle_tool(self):
        self.drawing_tools.set_tool('rounded_rectangle')

    def add_text(self, text, position):
        self.drawing_tools.add_text(text, position)

    def draw_line(self, start, end):
        self.drawing_tools.draw_line(start, end)

    def draw_curve(self, points):
        self.drawing_tools.draw_curve(points)

    def draw_rectangle(self, top_left, bottom_right):
        self.drawing_tools.draw_rectangle(top_left, bottom_right)

    def draw_polygon(self, points):
        self.drawing_tools.draw_polygon(points)

    def draw_ellipse(self, top_left, bottom_right):
        self.drawing_tools.draw_ellipse(top_left, bottom_right)

    def draw_rounded_rectangle(self, top_left, bottom_right, radius):
        self.drawing_tools.draw_rounded_rectangle(top_left, bottom_right, radius)

    def video_feed(self):
        ret, frame, gaze_coordinates = self.eye_tracker.get_frame()
        if ret:
            # Draw on the frame based on gaze coordinates
            if self.drawing_active:
                frame = self.drawing_tools.draw_on_frame(frame, gaze_coordinates)

            # Convert the frame to an image
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk

        # Repeat after an interval to capture the next frame
        self.root.after(10, self.video_feed)

    def run(self):
        self.root.mainloop()