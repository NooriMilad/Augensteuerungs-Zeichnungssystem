import Konva from 'konva';

document.addEventListener('DOMContentLoaded', () => {
    const notebookCanvas = document.getElementById('notebookCanvas') as HTMLDivElement;
    const eyeTrackingDataElement = document.getElementById('eyeTrackingData') as HTMLParagraphElement;
    const toggleDrawingButton = document.getElementById('toggleDrawing') as HTMLButtonElement;

    let drawingActive = false;
    let penColor = '#000000'; // Default color
    let strokeWidth = 5; // Default stroke width
    let gazeX = 0;
    let gazeY = 0;

    const stage = new Konva.Stage({
        container: 'notebookCanvas',
        width: window.innerWidth,
        height: window.innerHeight
    });

    const layer = new Konva.Layer();
    stage.add(layer);

    let isDrawing = false;
    let lastLine: Konva.Line;

    stage.on('mousedown touchstart', () => {
        if (!drawingActive) return;
        isDrawing = true;
        const pos = stage.getPointerPosition();
        if (pos) {
            lastLine = new Konva.Line({
                stroke: penColor,
                strokeWidth: strokeWidth,
                globalCompositeOperation: 'source-over',
                points: [pos.x, pos.y]
            });
            layer.add(lastLine);
        }
    });

    stage.on('mousemove touchmove', () => {
        if (!isDrawing) return;
        const pos = stage.getPointerPosition();
        if (pos) {
            const newPoints = lastLine.points().concat([pos.x, pos.y]);
            lastLine.points(newPoints);
            layer.batchDraw();
        }
    });

    stage.on('mouseup touchend', () => {
        isDrawing = false;
    });

    // Toggle drawing state
    toggleDrawingButton.addEventListener('click', () => {
        drawingActive = !drawingActive;
        toggleDrawingButton.innerHTML = drawingActive ? '<i class="fas fa-stop"></i> Stop' : '<i class="fas fa-play"></i> Start';
        fetch('/toggle_drawing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
    });

    // Color picker
    const penColorInput = document.getElementById('primaryColor') as HTMLInputElement;
    penColorInput.addEventListener('input', () => {
        penColor = penColorInput.value;
        fetch('/change_color', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ color: penColor })
        });
    });

    // Stroke width
    const strokeWidthInput = document.getElementById('strokeWidth') as HTMLInputElement;
    strokeWidthInput.addEventListener('input', () => {
        strokeWidth = parseInt(strokeWidthInput.value);
        fetch('/set_stroke_width', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ width: strokeWidth })
        });
    });

    // Tool selection
    const pencilToolButton = document.getElementById('pencilTool') as HTMLButtonElement;
    pencilToolButton.addEventListener('click', () => {
        stage.off('mousedown touchstart mousemove touchmove mouseup touchend');
        stage.on('mousedown touchstart', () => {
            if (!drawingActive) return;
            isDrawing = true;
            const pos = stage.getPointerPosition();
            if (pos) {
                lastLine = new Konva.Line({
                    stroke: penColor,
                    strokeWidth: strokeWidth,
                    globalCompositeOperation: 'source-over',
                    points: [pos.x, pos.y]
                });
                layer.add(lastLine);
            }
        });

        stage.on('mousemove touchmove', () => {
            if (!isDrawing) return;
            const pos = stage.getPointerPosition();
            if (pos) {
                const newPoints = lastLine.points().concat([pos.x, pos.y]);
                lastLine.points(newPoints);
                layer.batchDraw();
            }
        });

        stage.on('mouseup touchend', () => {
            isDrawing = false;
        });
    });

    const eraserToolButton = document.getElementById('eraserTool') as HTMLButtonElement;
    eraserToolButton.addEventListener('click', () => {
        stage.off('mousedown touchstart mousemove touchmove mouseup touchend');
        stage.on('mousedown touchstart', () => {
            if (!drawingActive) return;
            isDrawing = true;
            const pos = stage.getPointerPosition();
            if (pos) {
                lastLine = new Konva.Line({
                    stroke: 'white',
                    strokeWidth: strokeWidth,
                    globalCompositeOperation: 'destination-out',
                    points: [pos.x, pos.y]
                });
                layer.add(lastLine);
            }
        });

        stage.on('mousemove touchmove', () => {
            if (!isDrawing) return;
            const pos = stage.getPointerPosition();
            if (pos) {
                const newPoints = lastLine.points().concat([pos.x, pos.y]);
                lastLine.points(newPoints);
                layer.batchDraw();
            }
        });

        stage.on('mouseup touchend', () => {
            isDrawing = false;
        });
    });

    // Add event listeners for other tools as needed...

    // Eye tracking data
    function updateEyeTrackingData() {
        fetch('/get_eye_tracking_data')
            .then(response => response.json())
            .then(data => {
                const gazeCoordinates = data.gaze_coordinates;
                gazeX = gazeCoordinates[0];
                gazeY = gazeCoordinates[1];
                const direction = `Direction: (${gazeX}, ${gazeY})`;
                const percentage = `Percentage: ${Math.min(100, Math.max(0, Math.floor((gazeX / notebookCanvas.clientWidth) * 100)))}%`;
                eyeTrackingDataElement.textContent = `${direction}, ${percentage}`;

                if (drawingActive) {
                    const pos = { x: gazeX, y: gazeY };
                    if (isDrawing) {
                        const newPoints = lastLine.points().concat([pos.x, pos.y]);
                        lastLine.points(newPoints);
                        layer.batchDraw();
                    } else {
                        isDrawing = true;
                        lastLine = new Konva.Line({
                            stroke: penColor,
                            strokeWidth: strokeWidth,
                            globalCompositeOperation: 'source-over',
                            points: [pos.x, pos.y]
                        });
                        layer.add(lastLine);
                    }
                }
            });
    }

    setInterval(updateEyeTrackingData, 100); // Update every 100 milliseconds
});