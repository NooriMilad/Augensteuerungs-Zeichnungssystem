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