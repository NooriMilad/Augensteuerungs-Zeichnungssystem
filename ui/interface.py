import tkinter as tk
from tkinter import colorchooser, messagebox
from threading import Thread
import cv2
from PIL import Image, ImageTk

class UserInterface:
    def __init__(self, cursor_controller, drawing_tools):
        self.cursor_controller = cursor_controller
        self.drawing_tools = drawing_tools
        self.root = tk.Tk()
        self.root.title("Eye Tracking Communication System")
        self.root.geometry("1024x768")  # Set the window size
        self.drawing_active = False
        self.pen_color = "black"  # Default pen color

        # Create a toolbar frame
        self.toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Add a button to choose color
        self.color_button = tk.Button(self.toolbar, text="Choose Color", command=self.choose_color, font=("Helvetica", 12, "bold"))
        self.color_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Add a label to display the selected color
        self.color_label = tk.Label(self.toolbar, text="Selected Color: ", bg=self.pen_color, font=("Helvetica", 12, "bold"))
        self.color_label.pack(side=tk.LEFT, padx=2, pady=2)

        # Add a frame for the camera feed
        self.camera_frame = tk.Frame(self.root)
        self.camera_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add a label to display the camera feed
        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack()

        # Create a bottom frame for the buttons
        self.bottom_frame = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Add start and stop drawing buttons
        self.start_button = tk.Button(self.bottom_frame, text="Start Drawing", command=self.start_drawing, font=("Helvetica", 12, "bold"))
        self.start_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.stop_button = tk.Button(self.bottom_frame, text="Stop Drawing", command=self.stop_drawing, font=("Helvetica", 12, "bold"))
        self.stop_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Add a button to send a message
        self.message_button = tk.Button(self.bottom_frame, text="Send Message", command=self.send_message, font=("Helvetica", 12, "bold"))
        self.message_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Start the camera feed in a separate thread
        self.camera_thread = Thread(target=self.update_camera_feed)
        self.camera_thread.daemon = True
        self.camera_thread.start()

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code:
            self.pen_color = color_code[1]  # Get the hex color code
            self.drawing_tools.set_pen_color(self.pen_color)  # Update the pen color in drawing tools
            self.color_label.config(bg=self.pen_color)  # Update the color label background

    def start_drawing(self):
        self.drawing_active = True
        self.cursor_controller.eye_tracker.set_drawing_active(True)
        print("Drawing started")

    def stop_drawing(self):
        self.drawing_active = False
        self.cursor_controller.eye_tracker.set_drawing_active(False)
        print("Drawing stopped")

    def send_message(self):
        # Implement the logic to send a message
        messagebox.showinfo("Message Sent", "Your message has been sent to your family.")
        print("Message sent")

    def update_camera_feed(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (500, 500))  # Resize the frame to fit the label
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)

        cap.release()

    def run(self):
        self.root.mainloop()

class AccessibilitySettings:
    def __init__(self):
        # Initialize accessibility settings
        pass

    # Add methods to manage accessibility settings