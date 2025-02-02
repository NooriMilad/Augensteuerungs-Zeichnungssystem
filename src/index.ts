document.addEventListener('DOMContentLoaded', () => {
    const notebookCanvas = document.getElementById('notebookCanvas') as HTMLCanvasElement;
    const ctx = notebookCanvas.getContext('2d') as CanvasRenderingContext2D;
    const eyeTrackingDataElement = document.getElementById('eyeTrackingData') as HTMLParagraphElement;
    const toggleDrawingButton = document.getElementById('toggleDrawing') as HTMLButtonElement;

    let drawingActive = false;
    let currentTool = 'pencilTool'; // Default tool
    let penColor = '#000000'; // Default color
    let strokeWidth = 5; // Default stroke width
    let scale = 1; // Default scale for magnifier
    let gazeX = 0;
    let gazeY = 0;

    // Tool buttons
    const tools = [
        "freeFormSelect", "rectangularSelect", "eraser", "fillColor",
        "pickColorTool", "magnifier", "pencilTool", "paintBrush",
        "airBrushTool", "textTool", "lineTool", "curveTool",
        "rectangularTool", "polygon", "ellipseTool", "roundedRectangleTool"
    ];

    // Add event listeners to all tool buttons
    tools.forEach(tool => {
        const button = document.getElementById(tool) as HTMLButtonElement;
        button.addEventListener('click', () => {
            currentTool = tool;
            updateCursor(tool);
            fetch('/set_tool', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tool: tool })
            });
        });
    });

    // Update cursor based on selected tool
    function updateCursor(tool: string) {
        switch (tool) {
            case 'pencilTool':
            case 'paintBrush':
            case 'airBrushTool':
                notebookCanvas.style.cursor = 'url("https://cdn-icons-png.flaticon.com/512/60/60990.png"), auto';
                break;
            case 'eraser':
                notebookCanvas.style.cursor = 'url("https://cdn-icons-png.flaticon.com/512/60/60990.png"), auto';
                break;
            case 'textTool':
                notebookCanvas.style.cursor = 'text';
                break;
            case 'magnifier':
                notebookCanvas.style.cursor = 'zoom-in';
                break;
            default:
                notebookCanvas.style.cursor = 'crosshair';
                break;
        }
    }

    // Toggle drawing state
    toggleDrawingButton.addEventListener('click', () => {
        drawingActive = !drawingActive;
        toggleDrawingButton.innerHTML = drawingActive ? '<i class="fas fa-stop"></i>' : '<i class="fas fa-play"></i>';
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

    // Drawing functionality
    function draw() {
        if (!drawingActive) return;

        ctx.lineWidth = strokeWidth;
        ctx.lineCap = 'round';
        ctx.strokeStyle = penColor;

        if (currentTool === 'pencilTool' || currentTool === 'paintBrush') {
            ctx.lineTo(gazeX / scale, gazeY / scale);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(gazeX / scale, gazeY / scale);
        } else if (currentTool === 'eraser') {
            ctx.clearRect(gazeX / scale - strokeWidth / 2, gazeY / scale - strokeWidth / 2, strokeWidth, strokeWidth);
        }
    }

    // Eye tracking data
    function updateEyeTrackingData() {
        if (!drawingActive) return;

        fetch('/get_eye_tracking_data')
            .then(response => response.json())
            .then(data => {
                const gazeCoordinates = data.gaze_coordinates;
                gazeX = gazeCoordinates[0];
                gazeY = gazeCoordinates[1];
                const direction = `Direction: (${gazeX}, ${gazeY})`;
                const percentage = `Percentage: ${Math.min(100, Math.max(0, Math.floor((gazeX / 640) * 100)))}%`;
                eyeTrackingDataElement.textContent = `${direction}, ${percentage}`;

                if (drawingActive) {
                    draw();
                }
            });
    }

    setInterval(updateEyeTrackingData, 100); // Update every 100 milliseconds
});