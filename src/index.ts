document.addEventListener('DOMContentLoaded', () => {
    const toggleDrawingButton = document.getElementById('toggleDrawing') as HTMLButtonElement;
    const changeColorButton = document.getElementById('changeColor') as HTMLButtonElement;
    const penColorInput = document.getElementById('penColor') as HTMLInputElement;
    const eyeTrackingDataElement = document.getElementById('eyeTrackingData') as HTMLParagraphElement;
    const notebookCanvas = document.getElementById('notebookCanvas') as HTMLCanvasElement;
    const ctx = notebookCanvas.getContext('2d') as CanvasRenderingContext2D;

    let drawingActive = false;
    let penColor = penColorInput.value;

    toggleDrawingButton.addEventListener('click', () => {
        drawingActive = !drawingActive;
        alert('Drawing ' + (drawingActive ? 'enabled' : 'disabled'));
    });

    changeColorButton.addEventListener('click', () => {
        penColor = penColorInput.value;
        alert('Color changed to ' + penColor);
    });

    function updateEyeTrackingData() {
        fetch('/get_eye_tracking_data')
            .then(response => response.json())
            .then(data => {
                const gazeCoordinates = data.gaze_coordinates;
                const direction = `Direction: (${gazeCoordinates[0]}, ${gazeCoordinates[1]})`;
                const percentage = `Percentage: ${Math.min(100, Math.max(0, Math.floor((gazeCoordinates[0] / 640) * 100)))}%`;
                eyeTrackingDataElement.textContent = `${direction}, ${percentage}`;

                if (drawingActive) {
                    ctx.fillStyle = penColor;
                    ctx.beginPath();
                    ctx.arc(gazeCoordinates[0], gazeCoordinates[1], 5, 0, Math.PI * 2);
                    ctx.fill();
                }
            });
    }

    setInterval(updateEyeTrackingData, 1000); // Update every second
});