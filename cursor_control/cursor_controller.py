import pyautogui

class CursorController:
    def __init__(self, eye_tracker):
        self.eye_tracker = eye_tracker
        self.canvas = None

    def set_canvas(self, canvas):
        self.canvas = canvas

    def move_cursor(self, eye_position):
        if self.canvas and eye_position:
            x, y = eye_position
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            self.canvas.event_generate('<Motion>', warp=True, x=int(x * width), y=int(y * height))