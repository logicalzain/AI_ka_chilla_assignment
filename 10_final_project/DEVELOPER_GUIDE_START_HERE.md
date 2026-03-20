# 🚀 DEVELOPER GUIDE — Start Here!

Welcome! This guide explains everything about the JEEVES Desktop Assistant project. After reading this, you'll understand every aspect and be able to customize it completely.

---

## 🎯 What is JEEVES?

JEEVES is an **AI-powered desktop assistant** that:
- ✅ Listens to your voice commands
- ✅ Speaks back to you with AI responses
- ✅ Controls your PC (screenshots, battery, apps, etc.)
- ✅ Searches the web (Google, YouTube)
- ✅ Sends WhatsApp messages
- ✅ Plays games and tells jokes
- ✅ Connects to Arduino & ESP32 (IoT)
- ✅ Uses Google Gemini AI for smart answers

**Everything is customizable** — colors, voice, AI personality, commands, games, and more!

---

## 📁 Project Structure in 30 Seconds

```
10_final_project/
├── main.py                    ← RUN THIS TO START
├── config.json                ← CHANGE SETTINGS HERE
├── gui/
│   ├── app_gui.py            ← THE WINDOW & BUTTONS
│   └── voice_visualizer.py   ← THE ANIMATED ORB
├── core/
│   ├── assistant_core.py     ← THE BRAIN (COMMAND ROUTER)
│   └── voice_module.py       ← VOICE INPUT/OUTPUT
└── modules/
    ├── system_control.py     ← PC CONTROL
    ├── browser_control.py    ← WEB & WHATSAPP
    ├── arduino_control.py    ← IOT HARDWARE
    ├── ai_module.py          ← GEMINI AI
    └── games.py              ← GAMES & FUN
```

**Key Files You'll Edit:**
1. `config.json` — 90% of customizations
2. `gui/app_gui.py` — Colors, fonts, layout
3. `core/voice_module.py` — Voice settings
4. Module files — Add features

---

## 🎯 Getting Started (5 Minutes)

### Step 1: Run the App
```bash
python main.py
```

The window opens with:
- Left sidebar (quick buttons)
- Center (animated voice orb)
- Right (chat messages)
- Bottom (input bar)

### Step 2: Try Some Commands
```
Say or type:
- "battery"          # See battery %
- "time"             # Current time
- "tell joke"        # Random joke
- "play quiz"        # Trivia game
- "open chrome"      # Open browser
```

### Step 3: Look at config.json
Open `config.json` — this is where you customize EVERYTHING:
```json
{
    "assistant_name": "Jeeves",    // Change to "ARIA", "Bot", etc.
    "voice_rate": 180,             // Speed: 50-300
    "voice_volume": 1.0,           // Loudness: 0.0-1.0
    "voice_index": 0               // 0=Male, 1=Female
}
```

---

## 🎨 Customization Quick Starts

### "I want to change the COLORS"

**File to edit:** `gui/app_gui.py` (around line 23)

**Find this:**
```python
COLORS = {
    "accent": "#FF6600",        # Orange
    "bg_dark": "#0A0A0F",       # Dark background
    "text_primary": "#E8E8E8",  # Text color
    # ... more colors
}
```

**Change to:**
```python
COLORS = {
    "accent": "#0066FF",        # Blue (instead of orange)
    "bg_dark": "#FFFFFF",       # White background (light theme)
    "text_primary": "#000000",  # Black text
}
```

**Then run:** `python main.py`

**More color examples:**
- Purple theme: `"accent": "#9933FF"`
- Green theme: `"accent": "#00CC00"`
- Neon theme: `"accent": "#FF00FF", "listening": "#00FFFF"`

---

### "I want to change VOICE SETTINGS"

**File to edit:** `config.json`

**Voice SPEED** (voice_rate):
```json
"voice_rate": 100    // Slow & clear
"voice_rate": 180    // Normal (default)
"voice_rate": 250    // Fast
```

**Voice VOLUME** (voice_volume):
```json
"voice_volume": 0.3  // Quiet
"voice_volume": 0.7  // Medium
"voice_volume": 1.0  // Loud (default)
```

**Voice TYPE** (voice_index):
```json
"voice_index": 0     // Male (David) - professional
"voice_index": 1     // Female (Zira) - friendly
```

**Save config.json, restart the app!**

---

### "I want to add a SIDEBAR BUTTON"

**File to edit:** `gui/app_gui.py` (around line 68)

**Find:**
```python
SIDEBAR_BUTTONS = [
    ("🔋  Battery", "battery"),
    ("🕐  Time", "time"),
    # ...
]
```

**Add your button:**
```python
SIDEBAR_BUTTONS = [
    ("🔋  Battery", "battery"),
    ("🕐  Time", "time"),
    ("🎵  Spotify", "open spotify"),  # NEW BUTTON
    # ...
]
```

**Make sure** "open spotify" is a valid command in `core/assistant_core.py`!

---

### "I want to add a WEBSITE SHORTCUT"

**File to edit:** `modules/browser_control.py` (around line 27)

**Find:**
```python
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    # ... more websites
}
```

**Add:**
```python
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "mysite": "https://mysite.com",  # NEW
}
```

**Then say:** `open mysite`

---

### "I want to add an APP SHORTCUT"

**File to edit:** `modules/system_control.py` (around line 47)

**Find:**
```python
APP_COMMANDS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    # ... more apps
}
```

**Add:**
```python
APP_COMMANDS = {
    "notepad": "notepad.exe",
    "spotify": "spotify.exe",  # NEW
}
```

**Then say:** `open spotify`

---

## 💬 Adding Your Own Commands

### Example: Add a "Hello" Command

**Step 1:** Create function in `core/assistant_core.py`
```python
def _greet_user(name: str) -> str:
    """Greet the user by name."""
    return f"👋 Hello {name}! Nice to see you!"
```

**Step 2:** Add route in `process_command()` function
```python
# Add this in process_command():
if "hello" in command or "greet" in command:
    name = _extract_query(command, ["hello", "greet"])
    return _greet_user(name if name else "Friend")
```

**Step 3:** Add to help text (in `_get_help_text()`)
```
hello <name> — Greet you by name
```

**Step 4:** (Optional) Add sidebar button
```python
SIDEBAR_BUTTONS = [
    # ... other buttons
    ("👋 Hello", "hello"),  # NEW
]
```

**Test it:** Say "hello John" or type it in the chat!

---

## 🔊 Understanding Voice

### The Two Voice Processes:

**1. SPEAKING (TTS - Text to Speech)**
- Assistant speaks out loud
- Uses `pyttsx3` library
- Works OFFLINE ✅
- No internet needed

**2. LISTENING (STT - Speech to Text)**
- Records your microphone
- Sends to Google's free API
- Converts speech to text
- Needs INTERNET ❌

**Customize in `config.json`:**
- `voice_rate` — How fast to speak (50-300 WPM)
- `voice_volume` — How loud (0.0-1.0)
- `voice_index` — Male (0) or Female (1)

---

## 🤖 Understanding Commands

### How a Command Works:

```
1. User says: "What is Python?"
2. app_gui.py captures voice → "what is python?"
3. assistant_core.py.process_command() checks:
   - Is it a known command? NO
   - Do we have AI API key? YES
   - Ask permission: "Shall I use AI?"
4. User says: "yes"
5. ai_module.py sends to Google Gemini
6. AI responds: "Python is a programming language..."
7. GUI shows response in chat
8. TTS speaks the response
```

---

## 📊 Module Overview

### `core/assistant_core.py` — The Brain
- Routes ALL commands
- Decides where to send each command
- Handles "unknown command" scenarios
- Edit this to add commands

### `core/voice_module.py` — Voice Handler
- Text-to-Speech (speak)
- Speech-to-Text (listen)
- Edit this for voice problems

### `gui/app_gui.py` — The Window
- Creates the visual interface
- Handles button clicks
- Displays messages
- Edit this for colors, fonts, layout

### `modules/system_control.py` — PC Control
- Battery, time, date, screenshots
- Launch apps, lock PC, restart
- Edit this to add PC features

### `modules/browser_control.py` — Web
- Google search, YouTube
- Open websites, WhatsApp
- Edit this to add websites

### `modules/ai_module.py` — AI Brain
- Google Gemini integration
- Conversation memory
- Edit this to change AI model/personality

### `modules/games.py` — Fun Stuff
- Trivia, Hangman, Tic-Tac-Toe
- Jokes, dice, coin flip
- Edit this to add games/jokes

---

## ✅ Common Tasks

### Change the Theme Color
1. Open `gui/app_gui.py`
2. Find `COLORS = { ... }`
3. Change `"accent": "#FF6600"` to your color
4. Restart the app

### Add a Joke
1. Open `modules/games.py`
2. Find `JOKES = [ ... ]`
3. Add your joke: `"Why did...?"`
4. Restart the app
5. Say "tell joke"

### Add a Trivia Question
1. Open `modules/games.py`
2. Find `TRIVIA_QUESTIONS = [ ... ]`
3. Add new dict:
```python
{
    "question": "Your question?",
    "options": ["A", "B", "C", "D"],
    "answer": 1  # Index of correct answer
}
```
4. Say "play quiz"

### Change Window Size
1. Open `gui/app_gui.py`
2. Change:
```python
WINDOW_WIDTH = 1200   # Bigger width
WINDOW_HEIGHT = 800   # Bigger height
```
3. Restart the app

### Set Up Gemini AI
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Open `config.json`
5. Paste: `"gemini_api_key": "your-key-here"`
6. Restart the app
7. Now you can use AI commands!

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Colors not changing | Restart app with `python main.py` |
| Microphone not working | Check Windows Sound Settings |
| Speech recognition fails | Check internet connection |
| API key not working | Verify at https://aistudio.google.com/app/apikey |
| App won't start | Run `pip install -r requirements.txt` |
| PyAudio error | Run `pip install pipwin && pipwin install pyaudio` |

---

## 📚 Complete Documentation

For detailed information, read:
- **DOCUMENTATION.md** — Full developer guide (all details)
- **QUICK_REFERENCE.md** — Quick lookup guide
- **PROJECT_REPORT.md** — Hackathon submission report

---

## 🎯 Next Steps

1. **Run the app:** `python main.py`
2. **Change a color** in `gui/app_gui.py`
3. **Change voice settings** in `config.json`
4. **Add a command** in `core/assistant_core.py`
5. **Add a sidebar button** in `gui/app_gui.py`
6. **Read DOCUMENTATION.md** for everything else

---

## 💡 Pro Tips

✅ **Always restart the app** after editing code (`python main.py`)
✅ **Start small** — add one button, then one command
✅ **Test commands** by typing them (faster than voice)
✅ **Use the Help** — type "help" in the app to see all commands
✅ **Edit config.json for settings** (not code)
✅ **Keep backups** before major changes

---

## 🎓 Learning Path

1. **Understand the project** ← You are here!
2. Read `DOCUMENTATION.md` → Project Structure
3. Try changing colors
4. Try changing voice
5. Try adding a website
6. Try adding a command
7. Explore each module
8. Build your own feature

---

**You're ready to develop! Good luck! 🚀**

Need help? Check DOCUMENTATION.md or QUICK_REFERENCE.md!
