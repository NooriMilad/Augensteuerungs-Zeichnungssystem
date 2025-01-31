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
- Menschen mit Behinderungen neue kreative Möglichkeiten geben.
- Mehr Bewusstsein für Barrierefreiheit in der Technik schaffen.

## Installation und Ausführung

1. Erstelle und aktiviere eine virtuelle Umgebung:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # Auf Windows: .venv\Scripts\activate
    ```

2. Installiere die benötigten Abhängigkeiten:
    ```sh
    pip install -r requirements.txt
    ```

3. Starte das Projekt:
    ```sh
    python main.py
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
├── main.py
├── README.md
├── requirements.txt
├── src/
│   ├── cursor_control/
│   │   └── cursor_controller.py
│   ├── eye_tracking/
│   │   └── eye_tracker.py
│   ├── drawing_tools/
│   │   └── tools.py
│   ├── ui/
│   │   └── interface.py
│   └── accessibility/
│       └── settings.py
└── tests/
    └── test_main.py
