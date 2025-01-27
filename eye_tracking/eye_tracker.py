import mediapipe as mp
import cv2

class EyeTracker:
    def __init__(self, drawing_tools):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh()
        self.cap = None
        self.prev_eye_position = None
        self.drawing_tools = drawing_tools
        self.drawing_active = False

    def set_drawing_active(self, active):
        self.drawing_active = active

    def get_eye_position(self, frame):
        results = self.face_mesh.process(frame)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extract eye position from landmarks
                left_eye = face_landmarks.landmark[133]  # Example landmark for left eye
                right_eye = face_landmarks.landmark[362]  # Example landmark for right eye
                return (left_eye.x, left_eye.y), (right_eye.x, right_eye.y)
        return None, None

    def get_direction(self, prev_pos, curr_pos):
        if not prev_pos:
            return None
        dx = curr_pos[0] - prev_pos[0]
        dy = curr_pos[1] - prev_pos[1]
        if abs(dx) > abs(dy):
            return 'left' if dx < 0 else 'right'
        else:
            return 'up' if dy < 0 else 'down'

    def draw_direction(self, direction):
        if not self.drawing_active:
            return
        pen_color = self.drawing_tools.pen_color
        if direction == 'left':
            print(f"Drawing to the left with color {pen_color}")
            # Add your drawing logic here
        elif direction == 'right':
            print(f"Drawing to the right with color {pen_color}")
            # Add your drawing logic here
        elif direction == 'up':
            print(f"Drawing upwards with color {pen_color}")
            # Add your drawing logic here
        elif direction == 'down':
            print(f"Drawing downwards with color {pen_color}")
            # Add your drawing logic here

    def start_tracking(self, callback):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return

        eye_positions = []

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            left_eye, right_eye = self.get_eye_position(frame_rgb)
            if left_eye and right_eye:
                current_eye_position = ((left_eye[0] + right_eye[0]) / 2, (left_eye[1] + right_eye[1]) / 2)
                eye_positions.append(current_eye_position)
                callback(current_eye_position[0], current_eye_position[1])

                direction = self.get_direction(self.prev_eye_position, current_eye_position)
                if direction:
                    self.draw_direction(direction)
                self.prev_eye_position = current_eye_position

            cv2.imshow('Eye Tracking', frame)

            if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
                break

        self.cap.release()
        cv2.destroyAllWindows()
