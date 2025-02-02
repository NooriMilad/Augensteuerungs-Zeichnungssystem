# Wichtige Aspekte des Projekts

## Verwendung einer vortrainierten KI:
- **MediaPipe:** Dieses Projekt nutzt MediaPipe, eine vortrainierte KI-Bibliothek von Google, für die Augenverfolgung. MediaPipe bietet vorgefertigte Modelle für die Gesichts- und Augenverfolgung, die in Echtzeit arbeiten und eine präzise Erkennung der Augenbewegungen ermöglichen.

## GUI (Grafische Benutzeroberfläche):
- Die GUI wird mit HTML, CSS und JavaScript (TypeScript) erstellt und über Flask (Python) bereitgestellt. Sie ist responsiv und bietet eine intuitive Bedienung für die Zeichenwerkzeuge und die Augensteuerung.

## Konkretes Problem / Idee:
- Das Projekt löst das Problem der eingeschränkten Bewegungsfähigkeit bei Menschen, die traditionelle Zeichenwerkzeuge nicht verwenden können. Es ermöglicht ihnen, durch Augenbewegungen zu zeichnen und kreativ tätig zu sein.

## Verwendete Python-Bibliotheken:
- **OpenCV:** Für die Bildverarbeitung und die Integration der Augenverfolgung.
- **MediaPipe:** Für die Augenverfolgung und Gesichtserkennung.
- **Flask:** Für das Backend und die Bereitstellung der Webanwendung.
- **NumPy:** Für die Verarbeitung von Bilddaten.
- **PIL (Pillow):** Für die Bildmanipulation und das Zeichnen auf der Leinwand.

## Skizze der GUI:
- Die Benutzeroberfläche besteht aus einer Werkzeugleiste mit Zeichenwerkzeugen (z. B. Pinsel, Radierer, Füllfarbe), einer Leinwand zum Zeichnen und einem Bereich für die Live-Webcam-Ansicht zur Augenverfolgung. Sie ist einfach und barrierefrei gestaltet.

# Aufteilung der Aufgaben im Team

## Milad:
- Implementierung der Augenverfolgung mit MediaPipe und OpenCV.
- Integration der Augenverfolgung in die Zeichenfunktion.
- Entwicklung des Backends mit Flask für die Kommunikation zwischen Frontend und Augenverfolgung.

## Akif:
- Erstellung der GUI mit HTML, CSS und TypeScript.
- Implementierung der Zeichenwerkzeuge (Pinsel, Radierer, Füllfarbe usw.).
- Integration der Cursorsteuerung basierend auf den Augenbewegungen.

# Anleitung zur Ausführung des Codes

## Voraussetzungen:
- Python 3.x
- Node.js und npm
- Virtuelle Umgebung (optional, aber empfohlen)

## Installation:
1. Klonen des Repositorys: [https://github.com/NooriMilad/Augensteuerungs-Zeichnungssystem.git](https://github.com/NooriMilad/Augensteuerungs-Zeichnungssystem.git)
2. Wechseln in das Verzeichnis: 
    ```sh
    cd in das Verzeichnis
    ```
3. Erstellen und Aktivieren einer virtuellen Umgebung: 
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # Auf Windows: .venv\Scripts\activate
    ```
4. Installieren der Python-Abhängigkeiten: 
    ```sh
    pip install -r requirements.txt
    ```
5. Kompilieren des TypeScript-Codes: 
    ```sh
    npm install
    npm run build
    ```

## Starten der Anwendung:
1. Flask-Anwendung starten: 
    ```sh
    python app.py
    ```
2. Öffnen Sie Ihren Webbrowser und navigieren Sie zu [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Verwendung:
- Klicken Sie auf die **Start/Stop Zeichnen**-Taste, um den Zeichenmodus zu aktivieren.
- Verwenden Sie Ihre Augenbewegungen, um auf der Leinwand zu zeichnen.
- Wählen Sie Zeichenwerkzeuge aus der Werkzeugleiste aus und passen Sie die Farbe und Strichbreite an.
