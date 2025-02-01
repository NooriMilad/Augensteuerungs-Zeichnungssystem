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

        # Create a frame for the toolbar at the bottom
        self.toolbar_frame = ttk.Frame(self.main_frame)
        self.toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Add buttons to the toolbar
        self.add_toolbar_buttons()

        # Create a frame for the eye tracking data
        self.tracking_frame = ttk.Frame(self.main_frame)
        self.tracking_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Add labels for eye tracking data
        self.add_tracking_labels()

        # Initialize the webcam feed
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam.")
            self.root.destroy()
            return

        self.update_frame()

    def add_toolbar_buttons(self):
        # Add a button to change the pen color
        color_button = ttk.Button(self.toolbar_frame, text="Change Color", command=self.change_color)
        color_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Add a button to start/stop drawing
        draw_button = ttk.Button(self.toolbar_frame, text="Toggle Drawing", command=self.toggle_drawing)
        draw_button.pack(side=tk.LEFT, padx=2, pady=2)

    def add_tracking_labels(self):
        self.tracking_label = ttk.Label(self.tracking_frame, text="Eye Tracking Data", font=("Helvetica", 16))
        self.tracking_label.pack(pady=10)

        self.direction_label = ttk.Label(self.tracking_frame, text="Direction: N/A", font=("Helvetica", 14))
        self.direction_label.pack(pady=5)

        self.percentage_label = ttk.Label(self.tracking_frame, text="Percentage: N/A", font=("Helvetica", 14))
        self.percentage_label.pack(pady=5)

    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.drawing_tools.set_pen_color(color)

    def toggle_drawing(self):
        self.drawing_active = not self.drawing_active

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            if self.drawing_active:
                gaze_coordinates = self.eye_tracker.get_gaze_coordinates()
                self.drawing_tools.update_rectangle_position(gaze_coordinates)
                self.update_tracking_labels(gaze_coordinates)
            frame_with_rectangle = self.drawing_tools.draw_rectangle_on_frame(frame)
            img = Image.fromarray(cv2.cvtColor(frame_with_rectangle, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk  # Keep a reference to avoid garbage collection

        self.root.after(10, self.update_frame)

    def update_tracking_labels(self, gaze_coordinates):
        x, y = gaze_coordinates
        direction = f"Direction: ({x}, {y})"
        percentage = f"Percentage: {min(100, max(0, int((x / self.canvas.winfo_width()) * 100)))}%"
        self.direction_label.config(text=direction)
        self.percentage_label.config(text=percentage)

    def on_closing(self):
        if self.cap:
            self.cap.release()
        self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()