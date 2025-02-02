# filepath: /Users/marcoglavic/Documents/Augensteuerungs-Zeichnungssystem/app.py
from flask import Flask, render_template, Response, request, jsonify
import cv2
import mediapipe as mp
import pyautogui
from drawing_tools.tools import DrawingTools
from eye_tracking.eye_tracker import EyeTracker
from ui.interface import UserInterface

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
drawing_active = False

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
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
    return jsonify({'drawing_active': drawing_active})

@app.route('/change_color', methods=['POST'])
def change_color():
    color = request.json.get('color')
    drawing_tools.set_pen_color(color)
    return jsonify({'status': 'success'})

@app.route('/set_stroke_width', methods=['POST'])
def set_stroke_width():
    width = request.json.get('width')
    drawing_tools.set_stroke_width(width)
    return jsonify({'status': 'success'})

@app.route('/set_tool', methods=['POST'])
def set_tool():
    tool = request.json.get('tool')
    drawing_tools.set_tool(tool)
    return jsonify({'status': 'success'})

@app.route('/get_eye_tracking_data', methods=['GET'])
def get_eye_tracking_data():
    if not drawing_active:
        return jsonify({'gaze_coordinates': (0, 0)})

    ret, frame = camera.read()
    if not ret:
        return jsonify({'gaze_coordinates': (0, 0)})

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye = face_landmarks.landmark[468]
            left_eye_x = int(left_eye.x * screen_width)
            left_eye_y = int(left_eye.y * screen_height)
            return jsonify({'gaze_coordinates': (left_eye_x, left_eye_y)})

    return jsonify({'gaze_coordinates': (0, 0)})

if __name__ == '__main__':
    app.run(debug=True)