# 🏆 JEEVES — AI Desktop Assistant | Project Report

> **Presented by:** [Your Name]  
> **Course:** AI Ka Chilla — Final Project  
> **Date:** March 2026  
> **Version:** 4.0 (Hackathon Edition)

---

## 1. Project Overview

**JEEVES** is a fully functional AI-powered desktop assistant for Windows, built entirely with Python. It combines voice control, text commands, PC automation, IoT integration, and AI intelligence into a single application with a modern, animated GUI.

**Tagline:** *"Your Personal AI Desktop Assistant — Control Everything with Your Voice"*

### What Makes JEEVES Special

| Feature | Description |
|---------|-------------|
| 🎙️ Voice + Text | Dual input via microphone or keyboard |
| 🎭 Animated GUI | Jarvis/Siri-style pulsing orb with state animations |
| 🧠 AI Integration | Google Gemini API with **permission-based** usage |
| 💬 WhatsApp Messaging | Send messages to any phone number via command |
| 🔌 IoT Control | Arduino/ESP32 via Serial, Bluetooth, WiFi |
| 🎮 Built-in Games | 7 games + dice, coins, jokes, 8-ball |
| 🧰 Utility Toolkit | Calculator, password generator, uptime, quotes |
| 🔒 Privacy-First | AI asks permission before using API key |
| 📴 Offline Capable | Core features work without internet |

---

## 2. Problem Statement

Desktop users perform repetitive tasks daily: checking battery, opening apps, searching the web, controlling IoT devices, and finding information. Current solutions are either cloud-dependent (Alexa, Google Assistant) or limited in scope. **JEEVES solves this** by providing an all-in-one offline-first assistant that can extend to AI and IoT when needed.

---

## 3. Technical Architecture

```
┌─────────────┐    ┌──────────────────┐    ┌────────────────┐
│  User Input  │───▶│  AssistantCore   │───▶│  GUI Display   │
│  (Voice/Text)│    │  (Command Router)│    │  (CustomTkinter)│
└─────────────┘    └──────────────────┘    └────────────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  System  │ │ Browser  │ │ Arduino  │
        │ Control  │ │ Control  │ │ Control  │
        └──────────┘ └──────────┘ └──────────┘
              │           │           │
        ┌─────┘     ┌─────┘     ┌─────┘
        ▼           ▼           ▼
   Battery/Vol   Chrome     Serial/WiFi
   Screenshot    YouTube    LED/Motor
   Apps/Files    WhatsApp   Sensors
   Lock/Power    Google     ESP32
```

### Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Language | Python 3.11 | Cross-platform, rich ecosystem |
| GUI | CustomTkinter | Modern dark widgets, responsive |
| TTS | pyttsx3 | Offline, no API needed |
| STT | SpeechRecognition + Google | Accurate, free tier |
| AI | Google Gemini (gemini-2.0-flash) | Fast, capable, free tier |
| Serial | pyserial | Industry standard for Arduino |
| HTTP | requests | ESP32 WiFi endpoint calls |
| Browser | webbrowser | Built-in, reliable |
| System | psutil, pyautogui, winshell | PC control |
| Messaging | WhatsApp Web via wa.me URL | No dependencies needed |

---

## 4. Features in Detail

### 4.1 System Control (15+ commands)
- Battery status, time, date, screenshot
- System info (CPU, RAM, disk)
- Volume and brightness control
- Lock, shutdown, restart
- IP address, system uptime, OS info

### 4.2 Application Management
- Open any Windows app by name
- Kill/close applications
- Open folders and files
- Search for folders across drives

### 4.3 Web & Browser (20+ website shortcuts)
- Google search (explicit only)
- YouTube search/play
- Open Chrome, Gmail, GitHub, etc.
- 20+ built-in website shortcuts

### 4.4 WhatsApp Messaging
- Send messages to any phone number
- Uses wa.me deep-link (no extra dependencies)
- Supports all country codes
- Typo-tolerant ("watsapp" works too)

### 4.5 AI Integration (Permission-Based)
- Google Gemini for questions, research, code generation, summarization
- **Asks permission** before using API key
- Explicit commands bypass permission (ask, research, generate code)
- Falls back to "I'm not trained for this" when no AI available

### 4.6 Arduino & ESP32 IoT
- Serial communication (USB)
- WiFi HTTP commands (ESP32)
- Quick commands: LED on/off, Motor on/off
- Port auto-detection and status monitoring

### 4.7 Games & Entertainment
- Number Guessing, Trivia Quiz, Rock Paper Scissors
- Tic-Tac-Toe, Word Scramble, Math Challenge, Hangman
- Coin flip, dice roll, random number, Magic 8-Ball
- Jokes library

### 4.8 Utility Toolkit (NEW in v4)
- Math calculator (evaluate expressions)
- Password generator (custom length)
- System uptime tracker
- Motivational quotes
- Word/character counter
- Day-of-week calculator
- Clipboard copy to clipboard
- OS info

### 4.9 Voice Visualizer
- Custom-drawn animated orb (Jarvis/Siri-inspired)
- Three states: Idle (pulse), Listening (ripple), Speaking (waveform)
- Real-time state transitions tied to TTS/STT

---

## 5. GUI Design

- **Window:** 1000×620, centered, resizable (min 900×520)
- **Color scheme:** Deep navy-black (#0A0A0F) with bright orange (#FF6600) accents
- **Layout:** 3-panel design (Sidebar | Visualizer | Chat)
- **Fonts:** Segoe UI for labels, Cascadia Code for chat
- **Animations:** Canvas-based with 30 FPS rendering
- **Features:** Live clock, message counter, version badge, status bar indicators

---

## 6. Project Structure

```
10_final_project/
├── main.py                    # Entry point
├── config.json                # All settings
├── requirements.txt           # Pinned dependencies
├── DOCUMENTATION.md           # User documentation
├── PROJECT_REPORT.md          # This file
├── gui/
│   ├── app_gui.py             # GUI (578 lines)
│   └── voice_visualizer.py    # Animated orb (270 lines)
├── core/
│   ├── assistant_core.py      # Command router (665 lines)
│   └── voice_module.py        # TTS & STT (168 lines)
└── modules/
    ├── system_control.py      # PC control (460 lines)
    ├── browser_control.py     # Web automation (245 lines)
    ├── arduino_control.py     # IoT control (336 lines)
    ├── ai_module.py           # Gemini AI (248 lines)
    └── games.py               # Games/entertainment (800+ lines)
```

**Total:** ~3,700+ lines of Python code across 10 files

---

## 7. How to Run

```bash
conda activate ai_agents
pip install -r requirements.txt
python main.py
```

---

## 8. Future Improvements

These are potential enhancements that can extend JEEVES further:

| Improvement | Difficulty | Impact |
|-------------|-----------|--------|
| Email sending (SMTP) | Medium | High |
| Alarm/Timer with system notification | Easy | Medium |
| File search by content (grep) | Medium | High |
| Multi-language TTS | Easy | Medium |
| Dark/Light theme toggle | Easy | Low |
| Plugin system (load commands from .py files) | Hard | Very High |
| Calendar integration (Google Calendar API) | Medium | High |
| Music player (local files) | Medium | Medium |
| Screen recorder | Hard | High |
| Task scheduler (run commands at specific times) | Medium | High |
| Speech-to-text offline (Vosk) | Medium | High |
| Chat export to PDF | Easy | Low |
| Custom wake word ("Hey Jeeves") | Hard | Very High |

---

## 9. Deployment Options

### A. Run Locally (Recommended for Demo)
```bash
python main.py
```
Best for hackathon live demo. Fast, full-featured, all hardware works.

### B. Package as .exe (For Distribution)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="JEEVES" --icon=assets/icon.ico main.py
```
Creates a standalone .exe in `dist/` folder. Share with anyone — no Python needed.

### C. Upload to GitHub (For Judges to See Code)
```bash
git init
git add .
git commit -m "JEEVES v4.0 — AI Desktop Assistant"
git remote add origin https://github.com/your-username/jeeves-assistant.git
git push -u origin main
```

### D. Create a Demo Video
Record the screen while demonstrating:
1. Voice command (show visualizer animation)
2. Text command (search youtube mr beast)
3. WhatsApp messaging
4. AI permission flow
5. Calculator, password, quotes
6. Games (play a quick round)
7. Arduino LED control (if hardware available)

---

## 10. Conclusion

JEEVES is a comprehensive, production-quality desktop assistant that demonstrates:
- **Software Architecture**: Clean modular design with separation of concerns
- **AI Integration**: Real-world Gemini API usage with user consent
- **IoT**: Hardware communication via Serial and WiFi
- **GUI Development**: Custom animated widgets, responsive design
- **Natural Language Processing**: Smart keyword matching
- **Privacy**: Permission-based AI, offline-first design

It is ready for hackathon presentation and real-world use.

---

*Built with ❤️ using Python 3.11*
