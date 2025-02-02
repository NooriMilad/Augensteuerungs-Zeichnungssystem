import mediapipe as mp
import cv2

class EyeTracker:
    def __init__(self, drawing_tools):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True)
        self.cap = cv2.VideoCapture(0)  # Open the default camera
        self.prev_eye_position = None
        self.drawing_tools = drawing_tools
        self.drawing_active = False
        self.screen_width, self.screen_height = 640, 480  # Beispielwerte, anpassen nach Bedarf

    def set_drawing_active(self, active):
        self.drawing_active = active

    def get_eye_position(self, frame):
        results = self.face_mesh.process(frame)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extract eye position from landmarks
                left_eye = face_landmarks.landmark[133]  # Example landmark for left eye
                right_eye = face_landmarks.landmark[362]  # Example landmark for right eye
                left_eye_coords = (int(left_eye.x * frame.shape[1]), int(left_eye.y * frame.shape[0]))
                right_eye_coords = (int(right_eye.x * frame.shape[1]), int(right_eye.y * frame.shape[0]))
                # Draw circles on the eyes
                cv2.circle(frame, left_eye_coords, 5, (0, 255, 0), -1)
                cv2.circle(frame, right_eye_coords, 5, (0, 255, 0), -1)
                return left_eye_coords, right_eye_coords
        return None, None

    def release(self):
        self.cap.release()

    def update(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            eye_position = self.get_eye_position(frame)
            if eye_position:
                print(f"Left Eye: {eye_position[0]}, Right Eye: {eye_position[1]}")
            if eye_position and self.drawing_active:
                self.drawing_tools.draw(eye_position)
            cv2.imshow('Eye Tracker', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()
