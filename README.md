# Augensteuerungs-Zeichnungssystem

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

## Zusätzliche Ziele
- Die Technologie für Augensteuerung weiterentwickeln.

## Setup-Anleitung

### Voraussetzungen
- Python 3.x
- Node.js und npm
- Virtuelle Umgebung (optional, aber empfohlen)

### Installation

1. **Repository klonen**:
   ```sh
   git clone https://github.com/username/Augensteuerungs-Zeichnungssystem.git
   cd Augensteuerungs-Zeichnungssystem
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

5. Starte das Projekt:
    ```sh
    python app.py
    ```

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
