# Bachelorprojekt: Hexagon Puzzle

## Description
In this puzzle game, the primary objective is to insert differently shaped tiles, which
consist of blue and yellow-colored hexagons, into a given grid by rotating and flipping
them. To complete the puzzle, the yellow-colored hexagons must be placed in a
manner that allows them to form a coherent structure, such as a connected island
in the middle of the sea.

### Setup:

Installing Python 3.12 and run the following commands:

```bash
# creating virtual environment 
py -m venv .venv

# activate virtual environment 
.venv\Scripts\activate

# check for pip
py -m pip --version

# installing requirements
pip install -r requirements.txt

# deactivate virtual environment
deactivate
```

### Run:
```bash
.\.venv\Scripts\python.exe .\src\main.py
```

### Creating runnable:
```bash
pyinstaller main.spec
