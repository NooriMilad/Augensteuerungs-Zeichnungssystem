class DrawingTools:
    def __init__(self):
        self.current_tool = 'pencil'
        self.pen_color = (0, 0, 0)
        self.stroke_width = 5
        self.drawing_active = False

    def set_tool(self, tool):
        self.current_tool = tool

    def set_pen_color(self, color):
        self.pen_color = color

    def set_stroke_width(self, width):
        self.stroke_width = width

    def update_position(self, x, y):
        if self.drawing_active:
            # Implementieren Sie die Logik zum Zeichnen auf der Leinwand basierend auf den Koordinaten (x, y)
            pass