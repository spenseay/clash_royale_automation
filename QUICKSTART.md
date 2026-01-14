# Quick Start Guide

## Step 1: Install scrcpy (5 minutes)

1. Go to: https://github.com/Genymobile/scrcpy/releases
2. Download `scrcpy-win64-v2.x.zip` (the latest version)
3. Extract to `C:\scrcpy` (or anywhere you like)

## Step 2: Set up your Galaxy Tab

1. **Enable Developer Options:**
   - Settings → About tablet → Software information
   - Tap "Build number" 7 times (you'll see a countdown)

2. **Enable USB Debugging:**
   - Settings → Developer options
   - Turn ON "USB debugging"

3. **Connect via USB:**
   - Plug your tablet into your PC
   - Accept the "Allow USB debugging?" prompt on the tablet
   - Check "Always allow from this computer"

## Step 3: Test scrcpy

Open Command Prompt and run:
```
cd C:\scrcpy
scrcpy --window-title="ClashRoyale"
```

You should see your tablet screen appear in a window! Try touching the window with your mouse - it should control the tablet.

## Step 4: Install Python dependencies

Open Command Prompt in the project folder:
```
cd path\to\clash-automation
pip install -r requirements.txt
```

## Step 5: Open Clash Royale

1. Open Clash Royale on your tablet (via the scrcpy window)
2. Go to the **Training Camp** or **Test Arena** (this is important - don't test in real matches!)

## Step 6: Calibrate positions (optional but recommended)

The default card positions may not match your screen exactly. To calibrate:

```
python main.py --calibrate
```

This will let you move your mouse to different positions and see the percentage values. Update `config.py` with your values if needed.

## Step 7: Test a single deploy

```
python main.py --test
```

This will drag one card to see if everything is working.

## Step 8: Run continuously

```
python main.py
```

Cards will be deployed every 3 seconds. Press Ctrl+C to stop.

---

## Useful Commands

| Command | What it does |
|---------|--------------|
| `python main.py` | Run continuous deployment |
| `python main.py --test` | Deploy one card |
| `python main.py --calibrate` | Find screen positions |
| `python main.py --count 10` | Deploy exactly 10 cards |
| `python main.py --delay 1.5` | 1.5 second delay between deploys |
| `python main.py --random` | Random card/position selection |

---

## Troubleshooting

**"Window not found"**
- Make sure scrcpy is running
- Check that the window title includes "ClashRoyale"
- Try: `scrcpy --window-title="ClashRoyale"`

**Cards aren't landing in the right spot**
- Use `--calibrate` mode to find the correct positions
- Update the values in `config.py`

**scrcpy won't connect**
- Make sure USB debugging is enabled
- Try a different USB cable
- Run `adb devices` to check connection
- Some tablets need "USB configuration" set to MTP

**Mouse moves but nothing happens in game**
- Make sure the scrcpy window is in focus
- Try clicking on the scrcpy window first
