# Augensteuerungs-Zeichnungsprogramm

Dieses Projekt ist ein Augensteuerungs-Zeichnungsprogramm, das es Benutzern ermöglicht, mit ihren Augenbewegungen auf einer Leinwand zu zeichnen. Die Anwendung verwendet MediaPipe und OpenCV für die Augenverfolgung und bietet verschiedene Zeichenwerkzeuge.

## Projektteam
- Milad
- Akif

## Projektziel
Ein System entwickeln, mit dem Menschen durch ihre Augenbewegungen zeichnen können. Es soll besonders Menschen mit eingeschränkter Bewegungsfähigkeit helfen, kreativ zu sein.

## Zielgruppe
- Menschen mit eingeschränkter Bewegungsfähigkeit
- Künstler, die neue Zeichenmethoden ausprobieren möchten
- Entwickler und Forscher im Bereich Barrierefreiheit

## Hauptfunktionen
1. Augenverfolgung
2. Cursorsteuerung
3. Zeichenwerkzeuge
4. Benutzeroberfläche
5. Barrierefreiheit

## Funktionen

- **Augensteuerungs-Zeichnen**: Verwenden Sie Ihre Augenbewegungen, um auf der Leinwand zu zeichnen.
- **Zeichenwerkzeuge**: Beinhaltet Werkzeuge wie Bleistift, Pinsel, Radierer, Füllfarbe und mehr.
- **Responsive Benutzeroberfläche**: Die Benutzeroberfläche ist responsiv und funktioniert gut auf verschiedenen Bildschirmgrößen.
- **Zeichnen Starten/Stoppen**: Schalten Sie den Zeichenmodus mit der Start/Stop-Taste um.

## Zusätzliche Ziele
- Die Technologie für Augensteuerung weiterentwickeln.

## Setup-Anleitung

### Voraussetzungen
- Python 3.x
- Node.js und npm
- Virtuelle Umgebung (optional, aber empfohlen)

### Installation

1. Klonen Sie das Repository:
    ```sh
    git clone https://github.com/yourusername/eye-tracking-paint-program.git
    cd eye-tracking-paint-program
    ```

2. Erstelle und aktiviere eine virtuelle Umgebung:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # Auf Windows: .venv\Scripts\activate
    ```

3. Installiere die benötigten Abhängigkeiten:
    ```sh
    pip install -r requirements.txt
    ```

4. Kompiliere den TypeScript-Code:
    ```sh
    npm install
    npm run build
    ```

5. Starten Sie die Flask-Anwendung:
    ```sh
    python app.py
    ```

6. Öffnen Sie Ihren Webbrowser und navigieren Sie zu `http://127.0.0.1:5000/`.

## Verwendung

### Zeichnen Starten/Stoppen

- Klicken Sie auf die **Start/Stop Zeichnen**-Taste in der Werkzeugleiste, um den Zeichenmodus umzuschalten.
- Wenn der Zeichenmodus aktiv ist, werden Ihre Augenbewegungen verfolgt und zum Zeichnen auf der Leinwand verwendet.

### Zeichenwerkzeuge

- Wählen Sie ein Zeichenwerkzeug aus der Werkzeugleiste aus, um es zu verwenden.
- Verfügbare Werkzeuge sind:
  - Freiformauswahl
  - Rechteckauswahl
  - Radierer
  - Füllfarbe
  - Farbauswahl-Werkzeug
  - Lupe
  - Bleistift
  - Pinsel
  - Airbrush
  - Textwerkzeug
  - Linienwerkzeug
  - Kurvenwerkzeug
  - Rechteckwerkzeug
  - Polygon
  - Ellipsenwerkzeug
  - Abgerundetes Rechteckwerkzeug

### Farbe und Strichbreite

- Verwenden Sie den Farbwähler, um die Zeichenfarbe zu ändern.
- Passen Sie die Strichbreite mit dem Strichbreitenschieber an.

## Tests ausführen

1. Aktiviere die virtuelle Umgebung (falls noch nicht aktiviert):
    ```sh
    source .venv/bin/activate  # Auf Windows: .venv\Scripts\activate
    ```

2. Führe die Tests aus:
    ```sh
    python -m unittest discover tests
    ```

## Verzeichnisstruktur

```plaintext
Augensteuerungs-Zeichnungssystem/
├── .git
├── .venv
├── app.py
├── README.md
├── requirements.txt
├── src/
│   ├── cursor_control/
│   │   └── cursor_controller.py
│   ├── eye_tracking/
│   │   └── eye_tracker.py
│   ├── drawing_tools/
│   │   └── tools.py
├── static/
│   ├── styles.css
├── templates/
│   └── index.html
├── tsconfig.json
├── webpack.config.js
└── tests/
    ├── test_cursor_controller.py
    ├── test_eye_tracker.py
    └── test_tools.py
```

## Beitrag

Beiträge sind willkommen! Bitte öffnen Sie ein Issue oder reichen Sie einen Pull-Request für Verbesserungen oder Fehlerbehebungen ein.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

![Diagram des Programms](/Users/marcoglavic/Documents/Augensteuerungs-Zeichnungssystem/Augensteuerungs-Zeichnungssystem.png)