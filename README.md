# Clash Royale Test Automation

A learning project for building automation skills using Python, image recognition, and input simulation.

## Overview

This project automates interactions with Clash Royale's test arena by:
1. Mirroring your Galaxy Tab to your Windows PC
2. Capturing the screen to analyze game state
3. Detecting cards and their positions
4. Simulating drag actions to deploy troops

## Prerequisites

### 1. Install scrcpy (Screen Mirror Tool)

scrcpy lets you mirror and control your Android device from your PC.

**Installation:**
1. Download from: https://github.com/Genymobile/scrcpy/releases
2. Extract the zip file to a folder (e.g., `C:\scrcpy`)
3. Add that folder to your system PATH (optional, for convenience)

**Setup your Galaxy Tab:**
1. Enable Developer Options:
   - Go to Settings > About tablet
   - Tap "Build number" 7 times
2. Enable USB Debugging:
   - Go to Settings > Developer options
   - Turn on "USB debugging"
3. Connect via USB cable to your PC
4. Accept the debugging prompt on your tablet

**Test it:**
```bash
scrcpy
```
Your tablet screen should appear in a window on your PC!

### 2. Install Python (3.10+)

Download from: https://www.python.org/downloads/
- Check "Add Python to PATH" during installation

### 3. Install Project Dependencies

```bash
cd clash-automation
pip install -r requirements.txt
```

## Project Structure

```
clash-automation/
├── src/
│   ├── __init__.py
│   ├── screen_capture.py   # Screenshot and window management
│   ├── card_detector.py    # Finding cards using image recognition
│   ├── input_controller.py # Mouse/touch simulation
│   ├── game_state.py       # Track elixir, cards, etc. (future)
│   └── bot.py              # Main automation logic
├── assets/
│   └── templates/          # Card images for recognition
├── tests/
│   └── test_capture.py     # Test scripts
├── config.py               # Configuration settings
├── main.py                 # Entry point
├── requirements.txt
└── README.md
```

## Quick Start

### Step 1: Start scrcpy
```bash
scrcpy --window-title="ClashRoyale"
```

### Step 2: Open Clash Royale and go to the Test Arena

### Step 3: Capture a reference screenshot
```bash
python -m src.screen_capture --save-reference
```

### Step 4: Run the bot
```bash
python main.py
```

## How It Works

### Phase 1: Basic Card Dragging (Current)
- Finds the scrcpy window
- Locates card positions (bottom of screen)
- Drags a card to a target position in the arena
- Repeats on a timer

### Phase 2: Card Recognition (Future)
- Uses template matching to identify specific cards
- Selects cards strategically

### Phase 3: Game State Awareness (Future)
- Reads elixir count
- Tracks opponent's cards
- Makes decisions based on game state

## Configuration

Edit `config.py` to adjust:
- Window title for scrcpy
- Card slot positions
- Target drop zones
- Timing delays

## Troubleshooting

**scrcpy won't connect:**
- Make sure USB debugging is enabled
- Try a different USB cable
- Run `adb devices` to check connection

**Window not found:**
- Make sure scrcpy is running
- Check the window title matches config

**Cards not detected:**
- Capture new template images
- Adjust confidence threshold in config

## Learning Resources

- [scrcpy documentation](https://github.com/Genymobile/scrcpy)
- [OpenCV Python tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [PyAutoGUI documentation](https://pyautogui.readthedocs.io/)
