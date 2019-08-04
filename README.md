# UbiCut - The Mission Uncuttable Project

A video editing tool, that automatically cuts lectures.

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
```
git clone https://gitlab.imn.htwk-leipzig.de/weicker/mission-uncuttable.git
git checkout development
cd mission-uncuttable/code/
```
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
pip3 install wheel
pip3 install -r requirements.txt

```
## Projekt starten
```
fbs run
```

## Tests ausführen
```
fbs test
```

## Projekt für eigene Plattform freezen
```
fbs freeze
```

## Einen Installer für die eigene Plattform erstellen
```
fbs installer
```

## Das Installer Paket auf Debian/Ubuntu Installieren
```
sudo dpkg -i target/UbiCut.deb
```

## UbiCut auf Debian/Ubuntu deinstallieren
```
sudo dpkg --purge UbiCut
sudo rm -r ~/.config/ubicut
```

## Vor einem Commit
```
pip3 freeze > requirements.txt
```

# License
Copyright (C) 2019 mission-uncuttable

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
