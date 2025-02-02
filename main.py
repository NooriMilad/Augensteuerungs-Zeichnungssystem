import os
import logging
from flask import Flask, render_template, Response, request, jsonify
import cv2
import mediapipe as mp
import pyautogui
from eye_tracking.eye_tracker import EyeTracker
from drawing_tools.tools import DrawingTools
from cursor_control.cursor_controller import CursorController

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='dist', static_url_path='/static')

# MediaPipe Initialization
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Camera setup
camera = cv2.VideoCapture(0)

# Screen size for cursor control
screen_width, screen_height = pyautogui.size()

drawing_tools = DrawingTools()
eye_tracker = EyeTracker(drawing_tools)
cursor_controller = CursorController(eye_tracker)
drawing_active = False

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            eye_position = eye_tracker.get_eye_position(frame)
            if eye_position:
                cursor_controller.move_cursor(eye_position[0][0], eye_position[0][1])  # Move cursor based on eye position
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_drawing', methods=['POST'])
def toggle_drawing():
    global drawing_active
    drawing_active = not drawing_active
    eye_tracker.set_drawing_active(drawing_active)
    return jsonify({'drawing_active': drawing_active})

@app.route('/get_eye_tracking_data', methods=['GET'])
def get_eye_tracking_data():
    ret, frame = camera.read()
    if not ret:
        return jsonify({'gaze_coordinates': (0, 0)})
    frame = cv2.flip(frame, 1)
    left_eye_coords, right_eye_coords = eye_tracker.get_eye_position(frame)
    if left_eye_coords and right_eye_coords:
        return jsonify({'gaze_coordinates': left_eye_coords})
    return jsonify({'gaze_coordinates': (0, 0)})

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()