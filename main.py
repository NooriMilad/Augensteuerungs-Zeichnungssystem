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
drawing_active = True  # Start with drawing active

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
    drawing_active = request.json.get('drawing_active')
    eye_tracker.set_drawing_active(drawing_active)
    return jsonify({'drawing_active': drawing_active})

@app.route('/get_eye_tracking_data', methods=['GET'])
def get_eye_tracking_data():
    gaze_coordinates = eye_tracker.get_gaze_coordinates()
    return jsonify({'gaze_coordinates': gaze_coordinates})

# New endpoints for toolbar buttons
@app.route('/set_tool', methods=['POST'])
def set_tool():
    tool = request.json.get('tool')
    drawing_tools.set_tool(tool)
    return jsonify({'tool': tool})

@app.route('/change_color', methods=['POST'])
def change_color():
    color = request.json.get('color')
    drawing_tools.set_color(color)
    return jsonify({'color': color})

@app.route('/set_stroke_width', methods=['POST'])
def set_stroke_width():
    width = request.json.get('width')
    drawing_tools.set_stroke_width(width)
    return jsonify({'width': width})

@app.route('/fill_color', methods=['POST'])
def fill_color():
    color = request.json.get('color')
    drawing_tools.fill_color(color)
    return jsonify({'color': color})

@app.route('/pick_color', methods=['POST'])
def pick_color():
    color = drawing_tools.pick_color()
    return jsonify({'color': color})

@app.route('/magnify', methods=['POST'])
def magnify():
    drawing_tools.magnify()
    return jsonify({'status': 'magnified'})

@app.route('/air_brush', methods=['POST'])
def air_brush():
    drawing_tools.air_brush()
    return jsonify({'status': 'air brushed'})

@app.route('/add_text', methods=['POST'])
def add_text():
    text = request.json.get('text')
    position = request.json.get('position')
    drawing_tools.add_text(text, position)
    return jsonify({'text': text})

@app.route('/draw_line', methods=['POST'])
def draw_line():
    start = request.json.get('start')
    end = request.json.get('end')
    drawing_tools.draw_line(start, end)
    return jsonify({'status': 'line drawn'})

@app.route('/draw_curve', methods=['POST'])
def draw_curve():
    points = request.json.get('points')
    drawing_tools.draw_curve(points)
    return jsonify({'status': 'curve drawn'})

@app.route('/draw_rectangle', methods=['POST'])
def draw_rectangle():
    top_left = request.json.get('top_left')
    bottom_right = request.json.get('bottom_right')
    drawing_tools.draw_rectangle(top_left, bottom_right)
    return jsonify({'status': 'rectangle drawn'})

@app.route('/draw_polygon', methods=['POST'])
def draw_polygon():
    points = request.json.get('points')
    drawing_tools.draw_polygon(points)
    return jsonify({'status': 'polygon drawn'})

@app.route('/draw_ellipse', methods=['POST'])
def draw_ellipse():
    top_left = request.json.get('top_left')
    bottom_right = request.json.get('bottom_right')
    drawing_tools.draw_ellipse(top_left, bottom_right)
    return jsonify({'status': 'ellipse drawn'})

@app.route('/draw_rounded_rectangle', methods=['POST'])
def draw_rounded_rectangle():
    top_left = request.json.get('top_left')
    bottom_right = request.json.get('bottom_right')
    radius = request.json.get('radius')
    drawing_tools.draw_rounded_rectangle(top_left, bottom_right, radius)
    return jsonify({'status': 'rounded rectangle drawn'})

def main():
    app.run(debug=True, host='127.0.0.1', port=5000)
    eye_tracker.track_eyes()

if __name__ == '__main__':
    main()