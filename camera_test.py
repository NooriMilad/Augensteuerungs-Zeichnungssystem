import cv2

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    cv2.namedWindow('Camera Test', cv2.WINDOW_NORMAL)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            cv2.imshow('Camera Test', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Quit on 'q' key press
                break

            if cv2.getWindowProperty('Camera Test', cv2.WND_PROP_VISIBLE) < 1:
                break  # Window closed manually

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
