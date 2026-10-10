# Hanzi Matrix

A Chinese character learning animation inspired by *The Matrix*. Watch Chinese characters fall across the screen, with highlighted vocabulary, pinyin, and English meanings.

## Editions

- **Graphical edition — `hanzi-matrix-graphical-v4.py`**: A graphical animation with smooth movement, glowing characters, and red vocabulary highlights.
- **Terminal edition — `hanzi-matrix.py`**: A character-based animation designed to run inside a terminal.

## Requirements

- Python 3
- Linux desktop for the graphical edition
- Tkinter for the graphical edition
- A compatible terminal for the terminal edition

## Run on Linux

### 1. Install Python

On Ubuntu or Debian-based Linux, open a terminal and run:

```bash
sudo apt update
sudo apt install python3 python3-tk git
```

### 2. Download the project

```bash
git clone https://github.com/November717/hanzi-matrix.git
cd hanzi-matrix
```

### 3. Start the graphical edition

```bash
python3 hanzi-matrix-graphical-v4.py
```

A graphical desktop session is required.

### 4. Start the terminal edition

```bash
python3 hanzi-matrix.py
```

Run this command inside a terminal window. If your system reports a missing module or other error, check the error message and your Python environment.

## Controls

The program includes keyboard controls for vocabulary display and pinyin/English meaning display. Available controls may depend on the edition.

## Android and Termux

Android support is not yet guaranteed. The terminal edition may require changes for Termux compatibility, and the graphical edition requires a graphical environment or an Android-specific adaptation.

## Feedback

Try the project, explore the code, and share suggestions for improvements.
