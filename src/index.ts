import Konva from 'konva';

document.addEventListener('DOMContentLoaded', () => {
    const notebookCanvas = document.getElementById('notebookCanvas') as HTMLDivElement;
    const eyeTrackingDataElement = document.getElementById('eyeTrackingData') as HTMLInputElement;
    const toggleDrawingButton = document.getElementById('toggleDrawing') as HTMLButtonElement;
    const videoFeed = document.getElementById('videoFeed') as HTMLVideoElement;

    // Access the webcam
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
            videoFeed.srcObject = stream;
            videoFeed.play();
        });
    }

    let drawingActive = true; // Start drawing by default
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
    let newPoints: number[] = [];

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
        }
        layer.add(lastLine);
    });

    stage.on('mousemove touchmove', () => {
        if (!isDrawing) return;
        const pos = stage.getPointerPosition();
        if (pos) {
            const newPoints = lastLine.points().concat([pos.x, pos.y]);
            lastLine.points(newPoints);
            layer.batchDraw();
        }
        lastLine.points(newPoints);
        layer.batchDraw();
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
    const toolButtons = document.querySelectorAll('.toolbar button');
    toolButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tool = button.id;
            fetch(`/set_tool`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tool: tool })
            }).then(() => {
                // Update cursor based on the selected tool
                switch (tool) {
                    case 'pencilTool':
                        notebookCanvas.style.cursor = 'url(/static/cursors/pencil.cur), auto';
                        break;
                    case 'eraserTool':
                        notebookCanvas.style.cursor = 'url(/static/cursors/eraser.cur), auto';
                        break;
                    case 'textTool':
                        notebookCanvas.style.cursor = 'text';
                        break;
                    // Add cases for other tools as needed
                    default:
                        notebookCanvas.style.cursor = 'default';
                        break;
                }
            });
        });
    });

    const fillColorButton = document.getElementById('fillColor');
    if (fillColorButton) {
        fillColorButton.addEventListener('click', () => {
            fetch('/fill_color', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ color: penColor })
            });
        });
    }

    const pickColorTool = document.getElementById('pickColorTool');
    if (pickColorTool) {
        pickColorTool.addEventListener('click', () => {
            fetch('/pick_color', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
        });
    }

    const magnifier = document.getElementById('magnifier');
    if (magnifier) {
        magnifier.addEventListener('click', () => {
            fetch('/magnify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
        });
    }

    const airBrushTool = document.getElementById('airBrushTool');
    if (airBrushTool) {
        airBrushTool.addEventListener('click', () => {
            fetch('/air_brush', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
        });
    }

    const textTool = document.getElementById('textTool');
    if (textTool) {
        textTool.addEventListener('click', () => {
            const text = prompt('Enter text:');
            const position = { x: 50, y: 50 }; // Example position
            fetch('/add_text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text, position: position })
            });
        });
    }

    const lineToolElement = document.getElementById('lineTool');
    if (lineToolElement) {
        lineToolElement.addEventListener('click', () => {
            const start = { x: 10, y: 10 }; // Example start point
            const end = { x: 100, y: 100 }; // Example end point
            fetch('/draw_line', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ start: start, end: end })
            });
        });
    }

    const curveTool = document.getElementById('curveTool');
    if (curveTool) {
        curveTool.addEventListener('click', () => {
            const points = [{ x: 10, y: 10 }, { x: 50, y: 50 }, { x: 100, y: 10 }]; // Example points
            fetch('/draw_curve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ points: points })
            });
        });
    }

    const rectangularTool = document.getElementById('rectangularTool');
    if (rectangularTool) {
        rectangularTool.addEventListener('click', () => {
            const top_left = { x: 10, y: 10 }; // Example top left point
            const bottom_right = { x: 100, y: 100 }; // Example bottom right point
            fetch('/draw_rectangle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ top_left: top_left, bottom_right: bottom_right })
            });
        });
    }

    const polygonElement = document.getElementById('polygon');
    if (polygonElement) {
        polygonElement.addEventListener('click', () => {
            const points = [{ x: 10, y: 10 }, { x: 50, y: 50 }, { x: 100, y: 10 }]; // Example points
            fetch('/draw_polygon', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ points: points })
            });
        });
    }

    const ellipseTool = document.getElementById('ellipseTool');
    if (ellipseTool) {
        ellipseTool.addEventListener('click', () => {
            const top_left = { x: 10, y: 10 }; // Example top left point
            const bottom_right = { x: 100, y: 100 }; // Example bottom right point
            fetch('/draw_ellipse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ top_left: top_left, bottom_right: bottom_right })
            });
        });
    }

    const roundedRectangleTool = document.getElementById('roundedRectangleTool');
    if (roundedRectangleTool) {
        roundedRectangleTool.addEventListener('click', () => {
            const top_left = { x: 10, y: 10 }; // Example top left point
            const bottom_right = { x: 100, y: 100 }; // Example bottom right point
            const radius = 10; // Example radius
            fetch('/draw_rounded_rectangle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ top_left: top_left, bottom_right: bottom_right, radius: radius })
            });
        });
    }

    function updateEyeTrackingData() {
        fetch('/get_eye_tracking_data')
            .then(response => response.json())
            .then(data => {
                const gazeCoordinates = data.gaze_coordinates;
                gazeX = gazeCoordinates[0];
                gazeY = gazeCoordinates[1];
                const direction = `Direction: (${gazeX}, ${gazeY})`;
                const percentage = `Percentage: ${Math.min(100, Math.max(0, Math.floor((gazeX / notebookCanvas.clientWidth) * 100)))}%`;
                eyeTrackingDataElement.value = `${direction}, ${percentage}`;

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

    // Start drawing by default
    notebookCanvas.style.cursor = 'url(/static/cursors/pencil.cur), auto';
});