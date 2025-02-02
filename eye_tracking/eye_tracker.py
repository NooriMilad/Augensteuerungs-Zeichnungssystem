import mediapipe as mp
import cv2
import numpy as np

class EyeTracker:
    def __init__(self, drawing_tools):
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.drawing_tools = drawing_tools
        self.drawing_active = False
        self.gaze_coordinates = (0, 0)

    def get_eye_coordinates(self, results):
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye = face_landmarks.landmark[mp.solutions.face_mesh.FACEMESH_LEFT_EYE]
                right_eye = face_landmarks.landmark[mp.solutions.face_mesh.FACEMESH_RIGHT_EYE]
                left_eye_coords = (int(left_eye.x * 640), int(left_eye.y * 480))
                right_eye_coords = (int(right_eye.x * 640), int(right_eye.y * 480))
                self.gaze_coordinates = ((left_eye_coords[0] + right_eye_coords[0]) // 2,
                                         (left_eye_coords[1] + right_eye_coords[1]) // 2)
                return left_eye_coords, right_eye_coords
        return None, None

    def track_eyes(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.mp_face_mesh.process(frame_rgb)

            left_eye_coords, right_eye_coords = self.get_eye_coordinates(results)

            if left_eye_coords and right_eye_coords:
                cv2.circle(frame, left_eye_coords, 5, (0, 255, 0), -1)
                cv2.circle(frame, right_eye_coords, 5, (0, 255, 0), -1)
                print(f"Left Eye: {left_eye_coords}, Right Eye: {right_eye_coords}")

                if self.drawing_active:
                    self.drawing_tools.draw(left_eye_coords, right_eye_coords)

            cv2.imshow('Eye Tracking', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def get_gaze_coordinates(self):
        return self.gaze_coordinates

    def set_drawing_active(self, active):
        self.drawing_active = active

    def release(self):
        self.cap.release()
