# filepath: /Users/marcoglavic/Documents/Augensteuerungs-Zeichnungssystem/app.py
from flask import Flask, render_template, Response, request, jsonify
import cv2
from drawing_tools.tools import DrawingTools
from eye_tracking.eye_tracker import EyeTracker

app = Flask(__name__, static_folder='dist', static_url_path='/static')

camera = cv2.VideoCapture(0)
drawing_tools = DrawingTools()
eye_tracker = EyeTracker(drawing_tools)
drawing_active = False

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            if drawing_active:
                gaze_coordinates = eye_tracker.get_gaze_coordinates()
                drawing_tools.update_rectangle_position(gaze_coordinates)
            frame_with_rectangle = drawing_tools.draw_rectangle_on_frame(frame)
            ret, buffer = cv2.imencode('.jpg', frame_with_rectangle)
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

@app.route('/get_eye_tracking_data', methods=['GET'])
def get_eye_tracking_data():
    gaze_coordinates = eye_tracker.get_gaze_coordinates()
    return jsonify({'gaze_coordinates': gaze_coordinates})

if __name__ == '__main__':
    app.run(debug=True)