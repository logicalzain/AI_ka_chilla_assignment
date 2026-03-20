# 🤖 JEEVES Desktop Assistant — Complete Developer Documentation

> **Version:** 4.0 (Hackathon Edition) | **Python:** 3.11 | **Platform:** Windows 10/11

> **Purpose:** Comprehensive documentation for developers. Everything you need to understand, customize, and extend the JEEVES assistant.

---

## Table of Contents

1. [🚀 Quick Start](#-quick-start)
2. [📦 Installation](#-installation)
3. [▶️ Running the Assistant](#-running-the-assistant)
4. [📁 Project Structure & File Purposes](#-project-structure--file-purposes)
5. [🖥️ GUI Layout](#-gui-layout)
6. [⚙️ Configuration (config.json) — Complete Guide](#-configuration-configjson--complete-guide)
7. [🎨 Customization Guide — Colors, Voice, Fonts](#-customization-guide--colors-voice-fonts)
8. [📋 All Commands Reference](#-all-commands-reference)
9. [💬 WhatsApp Messaging](#-whatsapp-messaging)
10. [🤖 AI Permission System](#-ai-permission-system)
11. [🧰 Utility Toolkit](#-utility-toolkit)
12. [🎭 Voice Visualizer](#-voice-visualizer)
13. [👨‍💻 Developer Guide — How to Add Commands](#-developer-guide--how-to-add-commands)
14. [🔊 Voice System — Speech Recognition & Text-to-Speech](#-voice-system--speech-recognition--text-to-speech)
15. [🔌 Arduino & ESP32 Setup](#-arduino--esp32-setup)
16. [🤖 AI / Gemini Setup](#-ai--gemini-setup)
17. [🎮 Games & Entertainment](#-games--entertainment)
18. [🚀 Deployment Guide](#-deployment-guide)
19. [⚙️ How Commands Work Internally](#-how-commands-work-internally)
20. [🔧 Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

```bash
conda activate ai_agents
pip install -r requirements.txt
python main.py
```

---

## 📁 Project Structure & File Purposes

This section explains EXACTLY what each file and folder does, so you know where to make changes.

### Root Level Files

```
10_final_project/
├── main.py                    # ⭐ ENTRY POINT - Run this to start the app
├── config.json                # Settings file - customize voice, colors, API keys
├── requirements.txt           # List of all Python packages needed
├── DOCUMENTATION.md           # This file - Developer guide
├── DOCUMENTATION.pdf          # PDF version of docs
├── PROJECT_REPORT.md          # Hackathon submission report
└── project.txt                # (Empty placeholder)
```

#### **main.py** — The Starting Point
**Purpose:** This is the ONLY file you need to run. It initializes everything.

**What it does:**
1. Loads configuration from `config.json`
2. Initializes the `AssistantCore` from `core/assistant_core.py`
3. Launches the GUI (`gui/app_gui.py`)
4. Handles errors gracefully

**How to run:**
```bash
python main.py
```

**How to modify:**
- Change the `default_config` dictionary to update default settings
- Add new config keys here first, then use them in other modules

---

#### **config.json** — Your Settings File
**Purpose:** Store ALL customizable settings (voice, API keys, ports, paths).

**Why it exists:**
- Keep settings separate from code (easy to modify without programming)
- No need to restart the app for some settings
- Each user can have their own config

**All settings explained:**
```json
{
    // NAMES & IDENTITY
    "assistant_name": "Jeeves",      // What the assistant calls itself
    "user_name": "Boss",             // What the assistant calls you
    
    // VOICE SETTINGS (see Voice System section for details)
    "voice_rate": 180,               // Speaking speed: 50-300 (words per minute)
    "voice_volume": 1.0,             // 0.0 = silent, 1.0 = max volume
    "voice_index": 0,                // 0 = Male (David), 1 = Female (Zira)
    
    // AI SETUP (Google Gemini)
    "gemini_api_key": "",            // Get from: https://aistudio.google.com/app/apikey
    
    // HARDWARE (Arduino)
    "arduino_port": "COM3",          // Serial port (COM1-COM9 typical)
    "arduino_baud_rate": 9600,       // Data rate: 9600, 115200, etc.
    
    // IoT (ESP32 WiFi)
    "esp32_ip": "192.168.1.100",     // IP address of ESP32 on your network
    "esp32_port": 80,                // HTTP port (usually 80)
    
    // BROWSER
    "browser_path": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    
    // FILE SEARCH
    "search_directories": [          // Where to search for files
        "C:/Users",
        "D:/",
        "E:/"
    ],
    
    // SCREENSHOTS
    "screenshot_save_path": "",      // Leave empty = Desktop
    
    // UI
    "greeting_enabled": true         // Show greeting on startup
}
```

---

### **gui/** — Graphical User Interface (The Visual Part)

```
gui/
├── app_gui.py              # Main window, buttons, chat, layout
└── voice_visualizer.py     # The animated orb in the center
```

#### **gui/app_gui.py** — The Complete GUI Application
**Size:** ~400 lines | **Importance:** ⭐⭐⭐⭐⭐ (Core)

**What it does:**
- Creates the window and layout (sidebar | center orb | right chat)
- Handles button clicks
- Displays chat messages
- Manages input/output
- Runs the voice visualizer
- Updates status bar

**Structure inside:**
```python
COLORS = {...}              # Theme colors (customizable!)
FONTS = {...}              # Font definitions
WINDOW_WIDTH/HEIGHT        # Window size settings
SIDEBAR_BUTTONS            # Quick-action buttons
```

**How to customize:**
- **Change colors:** Edit the `COLORS` dictionary
- **Change window size:** Change `WINDOW_WIDTH` and `WINDOW_HEIGHT`
- **Add sidebar buttons:** Add to `SIDEBAR_BUTTONS` list
- **Change fonts:** Edit the `FONTS` dictionary

**Key methods:**
- `__init__()` — Initialize GUI
- `_build_header()` — Create title bar
- `_build_body()` — Create left/center/right panels
- `_add_bot_message()` — Show assistant response in chat
- `_on_send()` — Handle "send" button
- `_on_mic_click()` — Handle microphone button

---

#### **gui/voice_visualizer.py** — The Animated Orb
**Size:** ~200 lines | **Importance:** ⭐⭐⭐ (Visual Polish)

**What it does:**
- Draws the big animated circle in the center
- Changes color based on state (idle/listening/speaking)
- Adds animations (pulsing, ripples, waveform)
- Shows current time and status

**States & Colors:**
```python
STATE_COLORS = {
    "idle": "#FF6600",        # Orange - Waiting
    "listening": "#00E5FF",   # Cyan - Listening to microphone
    "speaking": "#FFB84D",    # Gold - Speaking (TTS)
}
```

**How to customize:**
- Change colors in `STATE_COLORS` dictionary
- Change animation speed: Look for `_animate()` method
- Change orb size: Modify canvas drawing commands

---

### **core/** — Core Brain & Voice

```
core/
├── assistant_core.py       # Command processor (main logic)
└── voice_module.py         # Speech recognition & text-to-speech
```

#### **core/assistant_core.py** — The Command Processor
**Size:** ~500+ lines | **Importance:** ⭐⭐⭐⭐⭐ (Critical)

**What it does:**
- Routes ALL commands to the right module
- Handles the "permission system" (ask AI permission)
- Extracts parameters from commands
- Provides help text
- Greets the user

**Key functions:**
- `process_command()` — Main router (if this says "battery", it calls system_control.get_battery_status())
- `_extract_query()` — Strips trigger words from commands
- `get_greeting()` — Friendly greeting message
- `_get_help_text()` — Lists all commands

**How it works internally:**
```
User says: "What is Python?"
    ↓
process_command("what is python?")
    ↓
Check: Is "python" a known command? NO
    ↓
Check: Do we have an AI API key? YES
    ↓
Ask permission: "Shall I use AI to answer?"
    ↓
If yes → AI responds
If no → "I'm not trained for this"
```

**How to add commands:**
1. Find the right section in `process_command()` (search for `# --- System Control ---`)
2. Add your command:
   ```python
   if "my trigger" in command or "alternate" in command:
       query = _extract_query(command, ["my trigger", "alternate"])
       return system_control.my_function(query)
   ```
3. Add help text in `_get_help_text()`
4. Add sidebar button in `gui/app_gui.py` (optional)

---

#### **core/voice_module.py** — Voice Input & Output
**Size:** ~150 lines | **Importance:** ⭐⭐⭐⭐ (Critical for voice)

**What it does:**
- `speak(text, config)` → Converts text to speech (TTS)
- `listen()` → Records microphone and converts to text (STT)
- `get_available_voices()` → Lists all voices on your system
- `reset_engine()` → Reset TTS engine

**How to customize voice:**

1. **Change voice speed** (voice_rate):
   - Config value: `voice_rate` (50-300 words per minute)
   - Current default: 180
   - Lower = Slower, Higher = Faster

2. **Change voice volume** (voice_volume):
   - Config value: `voice_volume` (0.0 to 1.0)
   - Current default: 1.0 (maximum)
   - 0.5 = Half volume, 0.0 = Silent

3. **Change voice type** (Male/Female):
   - Config value: `voice_index`
   - Index 0 = Male voice (David on Windows)
   - Index 1 = Female voice (Zira on Windows)
   - To see all voices: `python -c "import pyttsx3; e=pyttsx3.init(); [print(i,v.id) for i,v in enumerate(e.getProperty('voices'))]"`

**How to use:**
```python
from core.voice_module import speak, listen

# Speak text out loud
speak("Hello, how can I help?", config)

# Listen to microphone
text = listen()
if not text.startswith("[Error]"):
    print(f"You said: {text}")
```

**Important notes:**
- **TTS (speak)** works OFFLINE - no internet needed
- **STT (listen)** needs INTERNET - uses Google's free API
- Microphone must be connected and configured in Windows

---

### **modules/** — Feature Modules

```
modules/
├── system_control.py       # PC control (battery, screenshots, shutdown)
├── browser_control.py      # Web browser & WhatsApp
├── arduino_control.py      # Arduino & ESP32 IoT
├── ai_module.py            # Google Gemini AI integration
└── games.py                # Games & entertainment
```

#### **modules/system_control.py** — PC Control
**Size:** ~400 lines | **Importance:** ⭐⭐⭐⭐

**What it does:**
- Battery status
- Date & time
- Screenshots
- Empty recycle bin
- Lock/shutdown/restart PC
- Volume & brightness control
- System info (CPU, RAM, disk)
- Launch applications
- Open folders & files

**Key functions:**
- `get_battery_status()` → Battery %
- `get_current_time()` → Current time
- `take_screenshot()` → Save screenshot
- `open_app(app_name)` → Launch app
- `get_system_info()` → CPU/RAM/Disk
- And many more...

**How to customize:**

1. **Add a new app shortcut:**
   ```python
   APP_COMMANDS = {
       "existing apps": "...",
       "spotify": "spotify.exe",        # ADD THIS LINE
       "discord": "discord.exe",        # ADD THIS LINE
   }
   ```
   Then you can say: `open spotify` or `open discord`

2. **Change screenshot save location:**
   - Edit `config.json`: `"screenshot_save_path": "D:/MyScreenshots"`
   - Leave empty to use Desktop

3. **Add new feature:**
   - Create a function: `def my_feature() -> str:`
   - Import in `assistant_core.py`
   - Add route in `process_command()`

---

#### **modules/browser_control.py** — Web Browser & WhatsApp
**Size:** ~200 lines | **Importance:** ⭐⭐⭐

**What it does:**
- Open Chrome browser
- Google search
- YouTube search
- Open predefined websites
- WhatsApp Web messaging

**Built-in websites:**
```python
WEBSITES = {
    "youtube": "...",
    "google": "...",
    "gmail": "...",
    "github": "...",
    # And many more
}
```

**How to customize:**

1. **Add a new website shortcut:**
   ```python
   WEBSITES = {
       "existing": "...",
       "mysite": "https://mysite.com",  # ADD THIS
   }
   ```
   Then: `open mysite`

2. **Change Chrome path:**
   - Edit `config.json`: `"browser_path": "C:/path/to/chrome.exe"`

3. **Change browser:**
   - Modify `_get_browser()` function to use Firefox, Edge, etc.

---

#### **modules/ai_module.py** — Google Gemini AI
**Size:** ~250 lines | **Importance:** ⭐⭐⭐⭐ (Optional, but powerful)

**What it does:**
- Connect to Google Gemini AI
- Answer questions
- Research topics
- Generate code
- Summarize text
- Maintain conversation history

**Key customization points:**

1. **Change AI model:**
   ```python
   GEMINI_MODEL = "gemini-2.0-flash"  # Fast model
   GEMINI_MODEL = "gemini-2.0-pro"    # Smart but slower
   ```

2. **Change AI personality:**
   ```python
   SYSTEM_PROMPT = """You are Jeeves, a helpful assistant...
   Keep answers clear and concise."""
   ```

3. **Set API key:**
   - Go to: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy and paste in `config.json` under `gemini_api_key`
   - OR use the Settings panel in the app

---

#### **modules/arduino_control.py** — Arduino & ESP32 IoT
**Size:** ~300 lines | **Importance:** ⭐⭐⭐ (Optional, for hardware)

**What it does:**
- Connect to Arduino via USB (Serial)
- Send commands to Arduino
- Receive data from Arduino
- Connect to ESP32 via WiFi
- Toggle LEDs, motors, sensors

**How to customize:**

1. **Change Arduino port:**
   - Edit `config.json`: `"arduino_port": "COM3"`
   - Use `list ports` command to find your port

2. **Change baud rate:**
   - Edit `config.json`: `"arduino_baud_rate": 9600`
   - Must match your Arduino sketch

3. **Change ESP32 IP:**
   - Edit `config.json`: `"esp32_ip": "192.168.1.100"`

---

#### **modules/games.py** — Games & Entertainment
**Size:** ~400 lines | **Importance:** ⭐⭐⭐ (Fun stuff)

**What it does:**
- Number guessing
- Trivia quiz
- Rock-Paper-Scissors
- Tic-Tac-Toe
- Word scramble
- Math challenge
- Hangman
- Jokes
- Magic 8-Ball

**How to customize:**

1. **Add more trivia questions:**
   ```python
   TRIVIA_QUESTIONS = [
       {
           "question": "What is...?",
           "options": ["A", "B", "C", "D"],
           "answer": 1  # Index of correct answer (0, 1, 2, or 3)
       },
       # Add more...
   ]
   ```

2. **Add more jokes:**
   ```python
   JOKES = [
       "Existing jokes...",
       "Your new joke here",  # ADD THIS
   ]
   ```

3. **Add more hangman words:**
   ```python
   HANGMAN_WORDS = [
       "existing",
       "words",
       "newyourword",  # ADD THIS
   ]
   ```

---

## 📦 Installation

### Prerequisites

| Requirement | Details |
|------------|---------|
| **Python** | 3.11.x |
| **OS** | Windows 10 or 11 |
| **Microphone** | For voice commands only |
| **Internet** | For voice recognition & AI only |

### Install Steps

```bash
conda activate ai_agents
cd e:\programming\AI_ka_chilla_assignments\10_final_project
pip install -r requirements.txt
```

If PyAudio fails: `pip install pipwin && pipwin install pyaudio`

### All Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pyttsx3` | 2.98 | Offline TTS |
| `SpeechRecognition` | 3.11.0 | Voice input |
| `PyAudio` | 0.2.14 | Microphone |
| `customtkinter` | 5.2.1 | Modern GUI |
| `Pillow` | 10.4.0 | Images |
| `psutil` | 6.1.0 | System info |
| `pyautogui` | 0.9.54 | Screenshots |
| `pyperclip` | 1.9.0 | Clipboard |
| `winshell` | 0.6 | Recycle Bin |
| `pywin32` | 308 | Windows APIs |
| `comtypes` | 1.4.8 | Brightness |
| `pyserial` | 3.5 | Arduino |
| `requests` | 2.32.3 | ESP32 HTTP |
| `google-generativeai` | 0.8.3 | Gemini AI |

---

## ▶️ Running the Assistant

```bash
conda activate ai_agents
python main.py
```

| Shortcut | Action |
|---------|--------|
| `Enter` | Send command |
| `Ctrl+M` | Activate microphone |

---

## 🖥️ GUI Layout

```
┌─────────────────────────────────────────────────────┐
│  ⚡ JEEVES  AI Assistant  v4.0    [⚙️ Settings][🗑️]│
├────────┬──────────────────────┬─────────────────────┤
│⚡Quick │                      │ 💬 Command Log  12  │
│Actions │   🔮 VOICE ORB       │  chat messages…     │
│────────│   (big animated)     │                     │
│🔋Batt  │                      │                     │
│🕐Time  │   ● READY            │                     │
│📅Date  │  [🎤 Tap to Speak]   │                     │
│📸Snap  │   or press Ctrl+M    │                     │
│💻Info  │                      │ [Type command… Send]│
│⏱️Up   │  🕐 01:23 PM │ Mar 19│                     │
│────────│                      │                     │
│🌐Chrome│                      │                     │
│📺YT   │                      │                     │
│💬WA   │                      │                     │
│────────│                      │                     │
│🎮Games │                      │                     │
│😂Joke │                      │                     │
│🔑Pass  │                      │                     │
│📋Help  │                      │                     │
├────────┴──────────────────────┴─────────────────────┤
│ ✨ Ready    🤖 AI: ✅    🔌 Arduino: —              │
└─────────────────────────────────────────────────────┘
```

| Panel | Description |
|-------|-------------|
| **Left sidebar** | Quick-action buttons |
| **Center** | Big animated voice visualizer + mic + live clock |
| **Right** | Chat log + input bar |
| **Status bar** | Arduino/AI status indicators |

---

## 🎨 Customization Guide — Colors, Voice, Fonts

This section teaches you EXACTLY how to change the look and feel of the application.

### 🎨 How to Change Colors

All colors are defined in `gui/app_gui.py` in the `COLORS` dictionary (around line 23-42).

#### Theme Colors Dictionary
```python
COLORS = {
    # BACKGROUND COLORS
    "bg_dark": "#0A0A0F",           # Darkest background (main window)
    "bg_medium": "#12121A",         # Medium dark (panels)
    "bg_light": "#1A1A2E",          # Lighter (sections)
    "bg_card": "#16213E",           # Card/panel backgrounds
    
    # PRIMARY ACCENT (Orange by default)
    "accent": "#FF6600",            # Main accent color (buttons, highlights)
    "accent_hover": "#FF8533",      # When you hover over buttons
    "accent_dark": "#CC5200",       # Pressed/active state
    "accent_glow": "#FF660040",     # Transparent glow effect
    
    # TEXT COLORS
    "text_primary": "#E8E8E8",      # Main text (white-ish)
    "text_secondary": "#A0A0B0",    # Secondary text (gray)
    "text_muted": "#5A5A6E",        # Very faint text
    
    # STATUS COLORS
    "success": "#00E676",           # Green (success messages)
    "error": "#FF4444",             # Red (errors)
    
    # BORDERS & EFFECTS
    "border": "#2A2A3E",            # Border color
    "listening": "#00E5FF",         # Cyan (listening state)
    "header_bg": "#0F0F1A",         # Header background
    "sidebar_bg": "#0E0E18",        # Sidebar background
    "glow_orange": "#FF660025",     # Transparent orange glow
}
```

#### Quick Color Changes (Examples)

**Change accent color from orange to blue:**
```python
# Find this:
"accent": "#FF6600",            # Orange

# Change to:
"accent": "#0066FF",            # Blue
"accent_hover": "#3385FF",
"accent_dark": "#0052CC",
"listening": "#0066FF",         # Make listening cyan also blue
```

**Change accent color from orange to purple:**
```python
"accent": "#9933FF",            # Purple
"accent_hover": "#BB66FF",
"accent_dark": "#7722CC",
"accent_glow": "#9933FF40",
```

**Change accent color from orange to green:**
```python
"accent": "#00CC00",            # Green
"accent_hover": "#33FF33",
"accent_dark": "#009900",
"accent_glow": "#00CC0040",
```

**Change to dark mode with light text:**
```python
# Swap backgrounds
"bg_dark": "#FFFFFF",           # White background
"bg_medium": "#F5F5F5",
"text_primary": "#1A1A1A",      # Dark text
"text_secondary": "#555555",
```

**Make colors neon/bright:**
```python
"accent": "#FF00FF",            # Neon magenta
"listening": "#00FFFF",         # Neon cyan
"success": "#00FF00",           # Neon green
"error": "#FF0000",             # Neon red
```

#### How to Apply Color Changes
1. Open `gui/app_gui.py` in your code editor
2. Find the `COLORS = { ... }` dictionary (around line 23)
3. Change the hex color codes
4. Save the file
5. Run `python main.py` to see changes

#### How Color Codes Work
Colors are in **hexadecimal format**: `#RRGGBB`
- First 2 digits: RED (00-FF)
- Middle 2 digits: GREEN (00-FF)
- Last 2 digits: BLUE (00-FF)

Examples:
- `#FF0000` = Pure Red
- `#00FF00` = Pure Green
- `#0000FF` = Pure Blue
- `#FFFFFF` = White
- `#000000` = Black
- `#FF6600` = Orange (this project's default)

#### Recommended Color Palettes

**Dark Theme (Current):**
```python
"bg_dark": "#0A0A0F",
"accent": "#FF6600",
"text_primary": "#E8E8E8",
"success": "#00E676",
"error": "#FF4444",
```

**Light Theme:**
```python
"bg_dark": "#FFFFFF",
"bg_medium": "#F0F0F0",
"accent": "#0066FF",
"text_primary": "#000000",
"success": "#00AA00",
"error": "#AA0000",
```

**Purple Neon:**
```python
"bg_dark": "#0A0A15",
"accent": "#B500FF",
"accent_glow": "#B500FF30",
"listening": "#00FFFF",
```

---

### 🔊 How to Change Voice Settings

All voice settings are in `config.json`.

#### Voice Speed (voice_rate)
Controls how fast the assistant speaks.

```json
"voice_rate": 180
```

**Value ranges:**
- 50-100: Very slow, clear speech
- 100-150: Slow
- 150-200: Normal (180 is good default)
- 200-250: Fast
- 250-300: Very fast

**Examples:**
```json
"voice_rate": 100   # Slow, clear speech
"voice_rate": 150   # Slower than normal
"voice_rate": 180   # Normal (DEFAULT)
"voice_rate": 220   # Fast speech
"voice_rate": 300   # Very fast
```

#### Voice Volume (voice_volume)
Controls how loud the assistant speaks.

```json
"voice_volume": 1.0
```

**Value ranges:**
- 0.0: Silent (no sound)
- 0.1-0.3: Quiet
- 0.3-0.7: Normal but softer
- 0.7-1.0: Loud (1.0 is maximum)

**Examples:**
```json
"voice_volume": 0.3   # Quiet
"voice_volume": 0.5   # Half volume
"voice_volume": 0.8   # Loud
"voice_volume": 1.0   # Maximum (DEFAULT)
```

#### Voice Type (voice_index)
Choose between male and female voice.

```json
"voice_index": 0
```

**Available voices on Windows:**
- Index 0: Male voice (David) - DEFAULT
- Index 1: Female voice (Zira)

**To find all available voices on YOUR system:**
```bash
python -c "import pyttsx3; e=pyttsx3.init(); [print(i,v.id,v.name) for i,v in enumerate(e.getProperty('voices'))]"
```

**Examples:**
```json
"voice_index": 0   # Male voice (David)
"voice_index": 1   # Female voice (Zira)
```

---

### 🔤 How to Change Fonts

Fonts are defined in `gui/app_gui.py` in the `FONTS` dictionary (around line 44-59).

```python
FONTS = {
    "title": ("Segoe UI", 20, "bold"),
    "subtitle": ("Segoe UI", 10),
    "body": ("Segoe UI", 12),
    "body_bold": ("Segoe UI", 12, "bold"),
    "small": ("Segoe UI", 10),
    "chat": ("Cascadia Code", 11),
    "chat_fallback": ("Consolas", 11),
    "chat_name": ("Segoe UI", 11, "bold"),
    "button": ("Segoe UI", 11, "bold"),
    # And more...
}
```

**How to change a font:**
1. Font format: `("FontName", size, "weight")`
2. Example: `("Arial", 14, "bold")`

**Available fonts on Windows:**
- "Segoe UI" (recommended, modern)
- "Arial" (simple, classic)
- "Courier New" (monospace)
- "Georgia" (serif)
- "Times New Roman" (serif, classic)
- "Consolas" (monospace, code)
- "Cascadia Code" (monospace, modern)

**Font sizes:**
- 8-10: Small text
- 11-13: Body text
- 14-16: Subtitle
- 18-24: Title

**Font weights:**
- "normal" or no weight specified
- "bold" (thicker)
- "italic" (slanted)

**Change examples:**

```python
# Make title bigger
"title": ("Segoe UI", 28, "bold"),  # Was 20

# Use Arial instead of Segoe UI
"body": ("Arial", 12),  # Was "Segoe UI"

# Make chat text use monospace code font
"chat": ("Courier New", 12),  # Was "Cascadia Code"

# Use Georgia serif font for subtitle
"subtitle": ("Georgia", 10, "italic"),
```

---

### 🖼️ How to Customize the Voice Visualizer

The animated orb colors are in `gui/voice_visualizer.py` (around line 20-30).

```python
STATE_COLORS = {
    "idle": "#FF6600",        # Orange when waiting
    "listening": "#00E5FF",   # Cyan when listening
    "speaking": "#FFB84D",    # Gold when speaking
}
```

**Change the orb colors:**
```python
STATE_COLORS = {
    "idle": "#0066FF",        # Blue when waiting
    "listening": "#00FF00",   # Green when listening
    "speaking": "#FF00FF",    # Magenta when speaking
}
```

---

### 🎭 How to Customize the GUI Layout

#### Window Size
In `gui/app_gui.py` (around line 61-65):

```python
WINDOW_WIDTH = 1000      # Width in pixels
WINDOW_HEIGHT = 620      # Height in pixels
SIDEBAR_WIDTH = 160      # Left sidebar width
VIZ_PANEL_WIDTH = 290    # Center visualizer panel width
VISUALIZER_SIZE = 200    # Size of the animated orb
```

**Examples:**
```python
# Make window bigger for 4K monitors
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# Make window smaller for laptops
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

# Make sidebar wider
SIDEBAR_WIDTH = 220

# Make orb smaller
VISUALIZER_SIZE = 150
```

#### Sidebar Buttons
In `gui/app_gui.py` (around line 68-88):

```python
SIDEBAR_BUTTONS = [
    ("🔋  Battery", "battery"),
    ("🕐  Time", "time"),
    # ... more buttons
]
```

**How to add a button:**
```python
SIDEBAR_BUTTONS = [
    # ... existing buttons
    ("📊  Stats", "system info"),  # ADD THIS
]
```

Then the user can click the "📊 Stats" button to run the "system info" command.

**How to change button emoji or text:**
```python
# Change from:
("🔋  Battery", "battery"),

# Change to:
("🪫  Battery", "battery"),  # Different emoji
("⚡ PC Power", "battery"),    # Different text
```

#### Font Customization Example

Make all text bigger:
```python
FONTS = {
    "title": ("Segoe UI", 24, "bold"),        # Was 20
    "subtitle": ("Segoe UI", 12),             # Was 10
    "body": ("Segoe UI", 14),                 # Was 12
    "button": ("Segoe UI", 13, "bold"),       # Was 11
    # ... etc
}
```

---

### 📝 How to Customize Names & Identity

In `config.json`:

```json
{
    "assistant_name": "Jeeves",   # What the assistant calls itself
    "user_name": "Boss",          // What the assistant calls you
}
```

**Examples:**
```json
{
    "assistant_name": "ARIA",
    "user_name": "John",
}
```

Then:
- The window title will show: `⚡ ARIA — AI Desktop Assistant`
- The assistant might say: "Hi John, how can I help?"

---

## 📋 All Commands Reference

### 💻 System Control

| Command | What It Does |
|---------|-------------|
| `battery` | Battery %, charging, time left |
| `time` / `tell me the time` | Current time |
| `date` / `today` | Current date |
| `screenshot` | Save to Desktop |
| `system info` / `pc info` | CPU, RAM, Disk |
| `ip` / `my ip` | Hostname + IP |
| `empty recycle bin` | Empty Recycle Bin |
| `lock` / `lock pc` | Lock screen |
| `shutdown` / `restart` | Power + 30s delay |
| `cancel shutdown` | Cancel power action |
| `volume up/down/mute` | Volume control |
| `brightness up/down` | Brightness control |
| `uptime` | System boot time |
| `os info` / `windows version` | OS platform details |

### 📂 Files & Apps

| Command | What It Does |
|---------|-------------|
| `open <app>` | Open app |
| `close <app>` / `kill <app>` | Close app |
| `open folder <path>` | Open in Explorer |
| `open file <path>` | Open with default app |
| `search folder <name>` | Search for folder |

### 🌐 Web & Search

| Command | What It Does |
|---------|-------------|
| `search <anything>` | Google search |
| `<anything> on youtube` | YouTube search |
| `play <song/video>` | YouTube search |
| `open youtube/chrome/gmail` | Open website |
| `websites` | List all shortcuts |

### 💬 WhatsApp

| Command | What It Does |
|---------|-------------|
| `open whatsapp` | Open WhatsApp Web |
| `send whatsapp <phone> <msg>` | Send message |

### 🔌 Arduino / ESP32

| Command | What It Does |
|---------|-------------|
| `list ports` | List COM ports |
| `connect arduino [COMx]` | Connect serial |
| `send <cmd>` | Send to Arduino |
| `led on/off` | Quick LED toggle |
| `motor on/off` | Quick motor toggle |
| `wifi send <cmd>` | Send to ESP32 |
| `esp32 status` | Check reachability |

### 🤖 AI (Needs API Key)

| Command | Permission? |
|---------|------------|
| `ask <question>` | ❌ No |
| `research <topic>` | ❌ No |
| `generate code <desc>` | ❌ No |
| `summarize <text>` | ❌ No |
| Unknown command | ✅ Yes (asks first) |

### 🧰 Utilities (NEW!)

| Command | What It Does |
|---------|-------------|
| `calculate 5 + 3 * 2` | Math calculator |
| `generate password 20` | Random password |
| `uptime` | System boot time |
| `quote` / `motivate` | Inspirational quote |
| `count words <text>` | Word/char counter |
| `what day is 25-12-2024` | Day of week |
| `copy to clipboard <text>` | Clipboard copy |
| `os info` | Platform details |

### 🎮 Games

| Command | Game |
|---------|------|
| `play number guess` | Guess 1-100 |
| `play quiz` | Trivia quiz |
| `play rps` | Rock Paper Scissors |
| `play tictactoe` | Tic-Tac-Toe |
| `play scramble` | Word scramble |
| `play math` | Math challenge |
| `play hangman` | Hangman |
| `flip coin` / `roll dice` | Quick fun |
| `joke` | Random joke |
| `magic 8ball` | Ask the 8-Ball |

Type `quit` to exit any game.

---

## 💬 WhatsApp Messaging

### Format
```
send whatsapp <country_code><number> <message>
```

### Examples
```
send whatsapp 923001234567 Hello how are you?
send whatsapp +12025551234 Meeting at 5pm
send whatsapp 447911123456 See you tomorrow
```

| Country | Code |
|---------|------|
| Pakistan | 92 |
| USA | 1 |
| UK | 44 |
| India | 91 |

You must be logged into WhatsApp Web in your browser.

---

## 🤖 AI Permission System

**Unknown commands → JEEVES asks before using AI:**

```
You:    What is quantum physics?
Jeeves: 🤖 Shall I use AI to answer: "what is quantum physics"?
        Type yes or no.
You:    yes
Jeeves: [AI response]
```

**No API key? →** "I'm not trained for this" with suggestions.

**Direct AI commands** (ask, research, generate code, summarize) skip permission.

---

## 🧰 Utility Toolkit (NEW v4)

| Feature | Example | Output |
|---------|---------|--------|
| **Calculator** | `calculate 15 * 3 + 7` | 🧮 15 * 3 + 7 = 52 |
| **Password** | `generate password 20` | 🔑 Random 20-char password |
| **Uptime** | `uptime` | ⏱️ 5h 23m, booted at 4:15 PM |
| **Quote** | `quote` | 💡 "Talk is cheap. Show me the code." — Linus Torvalds |
| **Word Count** | `count words hello world` | 📊 Words: 2, Characters: 11 |
| **Day of Date** | `what day is 25-12-2024` | 📅 Wednesday, December 25, 2024 |
| **Clipboard** | `copy to clipboard Hello` | 📋 Copied! |
| **OS Info** | `os info` | 💻 Windows 10, AMD64 |

---

## 🎭 Voice Visualizer

The voice visualizer is the big animated orb in the center of the screen. It changes color based on what the assistant is doing.

| State | Animation | Color | Meaning |
|-------|-----------|-------|---------|
| Idle | Pulsing glow | 🟠 Orange | Waiting for input |
| Listening | Ripple rings | 🔵 Cyan | Microphone is active |
| Speaking | Waveform + particles | 🟠 Gold | Playing audio response |

**How to customize visualizer colors:**
- Edit `gui/voice_visualizer.py` around line 20-30
- Find `STATE_COLORS` dictionary
- Change hex color codes

Example:
```python
STATE_COLORS = {
    "idle": "#0066FF",        # Change to blue
    "listening": "#00FF00",   # Change to green
    "speaking": "#FF00FF",    # Change to magenta
}
```

---

## 🔊 Voice System — Speech Recognition & Text-to-Speech

This section explains how voice works and how to customize it.

### How Voice Works

The voice system has **TWO parts**:

1. **Text-to-Speech (TTS)** — Computer speaks to you
2. **Speech-to-Text (STT)** — Listens to you and converts to text

```
┌─────────────────────────────────────────────┐
│           VOICE SYSTEM                       │
├────────────────────┬────────────────────────┤
│                    │                        │
│ SPEAKING (TTS)     │ LISTENING (STT)        │
│ ─────────────────  │ ──────────────────     │
│ Text → Voice       │ Voice → Text           │
│ Uses pyttsx3       │ Uses SpeechRecognition │
│ Works OFFLINE ✅   │ Needs INTERNET ❌      │
│                    │                        │
└────────────────────┴────────────────────────┘
```

### Text-to-Speech (TTS) — How the Assistant Speaks

**Location:** `core/voice_module.py`

**Key function:**
```python
def speak(text: str, config: dict) -> None:
    """Convert text to speech and play through speakers."""
```

**Settings (in config.json):**
```json
{
    "voice_rate": 180,        // How fast to speak (50-300)
    "voice_volume": 1.0,      // How loud (0.0-1.0)
    "voice_index": 0          // Male=0, Female=1
}
```

#### Customizing TTS - Detailed

**SETTING 1: voice_rate (Speaking Speed)**

Controls words-per-minute. Default: 180

| Speed | voice_rate | Good for | Speed |
|-------|----------|----------|-------|
| Very Slow | 50-80 | Elderly users, clear speech | 🐢 🐢 🐢 |
| Slow | 80-120 | Easy to understand | 🐢 🐢 |
| Normal | 120-180 | General use | 🐢 |
| Fast | 180-240 | Impatient users | 🐇 |
| Very Fast | 240-300 | Quick responses | 🐇 🐇 🐇 |

**Change in config.json:**
```json
{
    "voice_rate": 100    // Slow and clear
}
```

**SETTING 2: voice_volume (Loudness)**

Controls volume. Default: 1.0 (maximum)

| Volume | voice_volume | When to use |
|--------|--------|-----------|
| Silent | 0.0 | Testing (no sound) |
| Quiet | 0.3 | Shared office, quiet mode |
| Normal | 0.5 | Default for most people |
| Loud | 0.8-0.9 | Noisy environment |
| Maximum | 1.0 | Presentations, big room |

**Change in config.json:**
```json
{
    "voice_volume": 0.5   // Half volume
}
```

**SETTING 3: voice_index (Voice Type)**

Choose male or female voice. Default: 0 (male)

**On Windows:**
- Index 0: **David** (Male) - Smooth, professional
- Index 1: **Zira** (Female) - Clear, friendly

**Change in config.json:**
```json
{
    "voice_index": 1   // Use Zira (female voice)
}
```

**Find more voices:**
If you have other voice packs installed (SAPI5 voices), run this to see all:
```bash
python -c "import pyttsx3; e=pyttsx3.init(); [print(f'{i}: {v.name}') for i,v in enumerate(e.getProperty('voices'))]"
```

**Example output:**
```
0: David (male)
1: Zira (female)
2: Mark (male, if installed)
3: Cortana (if installed)
```

### Speech-to-Text (STT) — How the Assistant Listens

**Location:** `core/voice_module.py`

**Key function:**
```python
def listen(timeout: int = 5, phrase_time_limit: int = 10) -> str:
    """Listen to microphone and convert speech to text."""
```

**How it works:**
1. Activates microphone
2. Waits for you to speak (max 5 seconds by default)
3. Records your voice (max 10 seconds)
4. Sends to Google's free Speech Recognition API
5. Returns text or error

**Settings:**
- `timeout` = How long to wait before giving up (default: 5 seconds)
- `phrase_time_limit` = Max length of one phrase (default: 10 seconds)

**Troubleshooting STT:**

| Problem | Cause | Solution |
|---------|-------|----------|
| "No speech detected" | Microphone not picking up | Speak louder, check Windows sound settings |
| "Could not understand" | Background noise | Reduce noise, speak clearly |
| "Speech service unavailable" | No internet | Connect to WiFi or mobile hotspot |
| "Microphone not found" | No microphone detected | Connect a microphone or enable built-in mic |

---

## ⚙️ Configuration (config.json) — Detailed Reference

```json
{
    "assistant_name": "Jeeves",
    "user_name": "Boss",
    "gemini_api_key": "",
    "voice_rate": 180,
    "voice_volume": 1.0,
    "voice_index": 0,
    "arduino_port": "COM3",
    "arduino_baud_rate": 9600,
    "esp32_ip": "192.168.1.100",
    "esp32_port": 80,
    "browser_path": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "search_directories": ["C:/Users"],
    "screenshot_save_path": "",
    "greeting_enabled": true
}
```

**See the "Customization Guide" section below for detailed settings explanations.**

---

## 👨‍💻 Developer Guide — How to Add Commands

### Step 1: Choose Your Module

| Module | Best For |
|--------|----------|
| `assistant_core.py` | Simple inline commands |
| `system_control.py` | PC/OS operations |
| `browser_control.py` | Web/URL operations |
| `arduino_control.py` | Hardware/IoT |
| `ai_module.py` | AI/API calls |
| `games.py` | Games/entertainment |

### Step 2: Write the Function

```python
# In modules/system_control.py (or wherever appropriate):
def my_new_feature(param: str) -> str:
    """What this feature does."""
    # Your logic here
    return f"✅ Result: {param}"
```

### Step 3: Add the Route

In `core/assistant_core.py` → `process_command()`, add:
```python
# My New Feature
if "my trigger" in command or "alternate trigger" in command:
    query = _extract_query(command, ["my trigger", "alternate trigger"])
    return system_control.my_new_feature(query)
```

### Step 4: Update Help Text

In `assistant_core.py` → `_get_help_text()`, add your command to the appropriate category.

### Step 5: Update Sidebar (Optional)

In `gui/app_gui.py` → `SIDEBAR_BUTTONS`:
```python
("🆕 My Feature", "my trigger"),
```

### Step 6: Update Documentation

Add the new command to this file and `PROJECT_REPORT.md`.

### Example: Adding a "Flip Text" Command

```python
# 1. In assistant_core.py, add these utility function:
def _flip_text(text: str) -> str:
    return f"🔄 Flipped: {text[::-1]}"

# 2. In process_command(), add route:
if "flip text" in command or "reverse text" in command:
    text = _extract_query(command, ["flip text", "reverse text"])
    return _flip_text(text) if text else "Try: flip text Hello World"

# 3. In _get_help_text(), add:
#   flip text <text> — Reverse text
```

---

## 🔌 Arduino & ESP32 Setup

### Arduino USB
```cpp
void setup() {
    Serial.begin(9600);
    pinMode(13, OUTPUT);
}
void loop() {
    if (Serial.available()) {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim();
        if (cmd == "LED_ON") { digitalWrite(13, HIGH); Serial.println("LED ON"); }
        else if (cmd == "LED_OFF") { digitalWrite(13, LOW); Serial.println("LED OFF"); }
    }
}
```

### ESP32 WiFi
Upload sketch with WiFi + WebServer on `/command?cmd=...`, then set `"esp32_ip"` in config.

---

## 🤖 AI / Gemini Setup

1. Get key: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Enter: ⚙️ Settings → Gemini API Key → Save

---

## 🎮 Games & Entertainment

Type your answer during games. Type `quit` to exit.
- Number Guess: a number (1-100)
- Quiz: A, B, C, D
- RPS: rock/paper/scissors
- Tic-Tac-Toe: 1-9
- Scramble: word guess
- Math: number
- Hangman: letter

---

## 🚀 Deployment Guide

### A. Local Demo (Best for Hackathon)
```bash
python main.py
```

### B. Package as .exe
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="JEEVES" main.py
# Output: dist/JEEVES.exe
```

### C. Upload to GitHub
```bash
git init
git add .
git commit -m "JEEVES v4.0"
git remote add origin https://github.com/you/jeeves.git
git push -u origin main
```

### D. Demo Video Tips
1. Show voice command with animated orb
2. Show text command (search, youtube, WhatsApp)
3. Show AI permission flow
4. Show calculator, password, quotes
5. Play a quick game
6. Show settings panel

---

## 📁 Project Structure

```
10_final_project/
├── main.py                    # Entry point
├── config.json                # Settings
├── requirements.txt           # Dependencies
├── DOCUMENTATION.md           # This file
├── PROJECT_REPORT.md          # Hackathon report
├── gui/
│   ├── app_gui.py             # GUI
│   └── voice_visualizer.py    # Animated orb
├── core/
│   ├── assistant_core.py      # Command router
│   └── voice_module.py        # TTS & STT
└── modules/
    ├── system_control.py      # PC control
    ├── browser_control.py     # Web + WhatsApp
    ├── arduino_control.py     # IoT
    ├── ai_module.py           # Gemini
    └── games.py               # Games
```

---

## ⚙️ How Commands Work Internally

```
User input (voice/text)
    ↓
app_gui.py → _execute_command()
    ↓ (background thread)
assistant_core.py → process_command()
    ├── Check AI permission state (yes/no pending?)
    ├── Check active game (route to game.play())
    ├── Keyword matching ("battery" in command)
    ├── Extract query (_extract_query strips triggers)
    ├── Route to module function
    ├── If unknown + AI → "Shall I use AI?" (yes/no)
    └── If unknown + no AI → "I'm not trained for this"
    ↓
Response → chat log + TTS speak (emoji stripped, max 500 chars)
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| PyAudio error | `pip install pipwin && pipwin install pyaudio` |
| No microphone | Check Windows Sound Settings |
| Voice recognition fails | Needs internet |
| TTS not working | Restart app |
| Arduino won't connect | Close IDE Serial Monitor |
| ESP32 unreachable | Check same WiFi + IP |
| AI not working | Check API key |
| WhatsApp not sending | Login to WhatsApp Web first |
| App crashes | Run in terminal to see error |
| "Not trained" | Use `search <query>` or set API key |
