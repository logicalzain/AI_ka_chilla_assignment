# ⚡ JEEVES Quick Reference Guide

**Need to change something? Find it here!**

---

## 🎯 Quick Navigation

### "I want to change the COLORS"
**File:** `gui/app_gui.py` (line 23-42)
**Key:** Edit the `COLORS` dictionary
```python
COLORS = {
    "accent": "#FF6600",           # Orange - CHANGE THIS
    "bg_dark": "#0A0A0F",          # Black - CHANGE THIS
    "text_primary": "#E8E8E8",     # White - CHANGE THIS
}
```
**Quick Examples:**
- Blue theme: `"accent": "#0066FF"`
- Purple theme: `"accent": "#9933FF"`
- Green theme: `"accent": "#00CC00"`

---

### "I want to change VOICE SPEED"
**File:** `config.json` (line 6)
**Key:** Change `voice_rate`
```json
"voice_rate": 180    // Default
"voice_rate": 100    // Slow & clear
"voice_rate": 250    // Fast
```
**Range:** 50-300 (words per minute)

---

### "I want to change VOICE VOLUME"
**File:** `config.json` (line 7)
**Key:** Change `voice_volume`
```json
"voice_volume": 1.0    // Loud (default)
"voice_volume": 0.5    // Half volume
"voice_volume": 0.3    // Quiet
```
**Range:** 0.0 (silent) to 1.0 (max)

---

### "I want to change MALE/FEMALE VOICE"
**File:** `config.json` (line 8)
**Key:** Change `voice_index`
```json
"voice_index": 0    // Male voice (David)
"voice_index": 1    // Female voice (Zira)
```

---

### "I want to add a NEW WEBSITE SHORTCUT"
**File:** `modules/browser_control.py` (line 27-48)
**Key:** Edit `WEBSITES` dictionary
```python
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "mysite": "https://mysite.com",   # ADD THIS
}
```
**Then say:** `open mysite`

---

### "I want to add a NEW APP SHORTCUT"
**File:** `modules/system_control.py` (line 47-67)
**Key:** Edit `APP_COMMANDS` dictionary
```python
APP_COMMANDS = {
    "notepad": "notepad.exe",
    "spotify": "spotify.exe",         # ADD THIS
}
```
**Then say:** `open spotify`

---

### "I want to add a SIDEBAR BUTTON"
**File:** `gui/app_gui.py` (line 68-88)
**Key:** Edit `SIDEBAR_BUTTONS` list
```python
SIDEBAR_BUTTONS = [
    ("🔋  Battery", "battery"),
    ("📊  MyButton", "my command"),   # ADD THIS
]
```

---

### "I want to add TRIVIA QUESTIONS"
**File:** `modules/games.py` (line 34+)
**Key:** Edit `TRIVIA_QUESTIONS` list
```python
TRIVIA_QUESTIONS = [
    {
        "question": "What is...?",
        "options": ["A", "B", "C", "D"],
        "answer": 1  # Index of correct answer
    },
]
```

---

### "I want to add JOKES"
**File:** `modules/games.py` (around line 350+)
**Key:** Edit `JOKES` list
```python
JOKES = [
    "Existing jokes...",
    "Your new joke here",   # ADD THIS
]
```

---

### "I want to change WINDOW SIZE"
**File:** `gui/app_gui.py` (line 61-65)
**Key:** Change WINDOW_WIDTH and WINDOW_HEIGHT
```python
WINDOW_WIDTH = 1000    # Change to 1200, 800, etc.
WINDOW_HEIGHT = 620    # Change to 900, 500, etc.
```

---

### "I want to change FONTS"
**File:** `gui/app_gui.py` (line 44-59)
**Key:** Edit `FONTS` dictionary
```python
FONTS = {
    "title": ("Segoe UI", 20, "bold"),
    # Change "Segoe UI" to "Arial", "Georgia", etc.
    # Change 20 to bigger/smaller size
}
```

---

### "I want to change the ORBE COLOR"
**File:** `gui/voice_visualizer.py` (line 20-30)
**Key:** Edit `STATE_COLORS` dictionary
```python
STATE_COLORS = {
    "idle": "#FF6600",        # Orange - CHANGE THIS
    "listening": "#00E5FF",   # Cyan - CHANGE THIS
    "speaking": "#FFB84D",    # Gold - CHANGE THIS
}
```

---

### "I want to change ASSISTANT/USER NAMES"
**File:** `config.json` (line 2-3)
**Key:** Change `assistant_name` and `user_name`
```json
"assistant_name": "ARIA",     # Change from "Jeeves"
"user_name": "John",          # Change from "Boss"
```

---

### "I want to set up GOOGLE GEMINI AI"
**File:** `config.json` (line 5)
**Key:** Add `gemini_api_key`
```json
"gemini_api_key": "your-api-key-here"
```
**Get key from:** https://aistudio.google.com/app/apikey

---

### "I want to change ARDUINO PORT"
**File:** `config.json` (line 9)
**Key:** Change `arduino_port`
```json
"arduino_port": "COM3"    // Change to your port
```
**Find your port:** Type `list ports` in the app

---

### "I want to change ESP32 IP ADDRESS"
**File:** `config.json` (line 11)
**Key:** Change `esp32_ip`
```json
"esp32_ip": "192.168.1.100"   // Change to your IP
```

---

### "I want to add a NEW COMMAND"
**Steps:**
1. Create function in the right module (e.g., `modules/system_control.py`)
2. Add route in `core/assistant_core.py` → `process_command()`
3. Add help text in `core/assistant_core.py` → `_get_help_text()`
4. (Optional) Add sidebar button in `gui/app_gui.py` → `SIDEBAR_BUTTONS`

**Example:** Adding "flip text" command
```python
# In core/assistant_core.py, add this:
if "flip text" in command or "reverse" in command:
    text = _extract_query(command, ["flip text", "reverse"])
    return text[::-1] if text else "What text?"
```

---

### "I want to TAKE A SCREENSHOT"
**File:** `config.json` (line 18)
**Key:** Change `screenshot_save_path`
```json
"screenshot_save_path": ""           // Desktop
"screenshot_save_path": "D:/Shots"   // Custom folder
```

---

### "I want to CHANGE THE AI MODEL"
**File:** `modules/ai_module.py` (line 32-33)
**Key:** Change `GEMINI_MODEL`
```python
GEMINI_MODEL = "gemini-2.0-flash"   # Fast
GEMINI_MODEL = "gemini-2.0-pro"     # Smart (slower)
```

---

### "I want to CHANGE THE AI PERSONALITY"
**File:** `modules/ai_module.py` (line 36-40)
**Key:** Change `SYSTEM_PROMPT`
```python
SYSTEM_PROMPT = """You are a helpful assistant.
Keep answers short and friendly."""
```

---

## 📊 File Reference

| File | Purpose | Edit For |
|------|---------|----------|
| `main.py` | Entry point | Default settings |
| `config.json` | Settings | Voice, API key, paths |
| `gui/app_gui.py` | Window & layout | Colors, fonts, buttons, size |
| `gui/voice_visualizer.py` | Animated orb | Orb colors |
| `core/assistant_core.py` | Command router | Add commands, help text |
| `core/voice_module.py` | Voice I/O | Voice settings |
| `modules/system_control.py` | PC control | Apps, system functions |
| `modules/browser_control.py` | Web browser | Websites |
| `modules/ai_module.py` | AI (Gemini) | AI model, personality |
| `modules/arduino_control.py` | Arduino/ESP32 | Hardware settings |
| `modules/games.py` | Games & fun | Trivia, jokes, games |

---

## 🎨 Color Quick Reference

```
#FF6600  = Orange (current accent)
#0066FF  = Blue
#9933FF  = Purple
#00CC00  = Green
#FF0000  = Red
#00FF00  = Bright green
#00FFFF  = Cyan
#FF00FF  = Magenta
#FFFFFF  = White
#000000  = Black
#FFB84D  = Gold
#E8E8E8  = Light gray (text)
```

---

## 🔊 Voice Settings Quick Reference

```
voice_rate examples:
50-80    = Very slow & clear (🐢🐢🐢)
100-150  = Slow (🐢🐢)
180      = Normal (🐢)
200-250  = Fast (🐇)
300      = Very fast (🐇🐇🐇)

voice_volume examples:
0.0      = Silent (testing)
0.3      = Quiet (office)
0.5      = Normal (most people)
0.8      = Loud (noisy room)
1.0      = Maximum (presentations)

voice_index:
0        = David (male, professional)
1        = Zira (female, friendly)
```

---

## 🔧 Troubleshooting Quick Links

- **Colors not changing?** Restart the app with `python main.py`
- **Voice not working?** Check microphone in Windows Sound Settings
- **Microphone can't hear?** Speak louder or reduce background noise
- **API key not working?** Check at https://aistudio.google.com/app/apikey
- **Arduino won't connect?** Close Arduino IDE first
- **Missing packages?** Run `pip install -r requirements.txt`

---

## 🚀 Quick Commands to Try

```
Say or type these:
- "battery"           # Battery status
- "time"              # Current time
- "screenshot"        # Take screenshot
- "open chrome"       # Open browser
- "search google"     # Google search
- "open youtube"      # Open YouTube
- "play quiz"         # Play trivia game
- "flip coin"         # Flip a coin
- "tell joke"         # Get a joke
- "help"              # Show all commands
```

---

## 📚 Where to Find Everything in DOCUMENTATION.md

| Topic | Section |
|-------|---------|
| Project structure | 📁 Project Structure & File Purposes |
| Color customization | 🎨 Customization Guide |
| Voice customization | 🔊 Voice System |
| Adding commands | 👨‍💻 Developer Guide |
| Arduino setup | 🔌 Arduino & ESP32 Setup |
| AI setup | 🤖 AI / Gemini Setup |
| Games | 🎮 Games & Entertainment |
| Troubleshooting | 🔧 Troubleshooting |

---

**Need more detail? Check DOCUMENTATION.md for complete information!**
