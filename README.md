# The Mission Uncuttable Project

## Team

- Sascha Rittig - *Product Owner*
- Tim Jeske - *Software Architect*
- Felix Dittrich
- Clemens Zwinzscher
- Maximilian Fornacon
- Johannes Müller
- Julian Oliver Böttcher
- Valentin Ackva
- Alexander Bonin
- Markus Leupold
- Jeremy Risy

## Setup
Enviroment erschaffen:
```
python3 -m venv venv
```
Für Mac/Linux:
```
source venv/bin/activate
```
Für Windows:
```
call venv\scripts\activate.bat
```
Bibliotheken installieren:
```
pip install fbs PyQt5==5.9.2 PyInstaller==3.4
pip3 install -r requirements.txt

```
## Projekt starten
```
fbs run
```

## Projekt für eigene Plattform freezen
```
fbs freeze
```

## Einen Installer für die eigene Plattform erstellen
```
fbs installer

```
