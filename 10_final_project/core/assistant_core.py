# ============================================================
# assistant_core.py — Central Command Router (The Brain)
# ============================================================
# v4 (Hackathon Edition): Smart matching + AI permission + extras
#
# KEY BEHAVIORS:
#   1. Keyword matching (flexible, natural language)
#   2. Google search ONLY when user says "search" / "google"
#   3. AI used ONLY after asking user permission
#   4. Unknown → "I'm not trained for this" (no auto-search)
#   5. WhatsApp messaging via wa.me deep-link
#   6. NEW: Calculator, password gen, uptime, quotes, clipboard
#
# HOW TO ADD A NEW COMMAND (Developer Guide):
#   1. Find the appropriate section in process_command()
#   2. Add:  if "your_trigger" in command:
#               return your_function()
#   3. Add the function either here or in a module file
#   4. Update _get_help_text() with the new command description
# ============================================================

import json
import os
import datetime
import re
import random
import string
import math
import platform

from modules import system_control
from modules import browser_control
from modules import arduino_control
from modules import ai_module
from modules import games


def _extract_query(command: str, triggers: list) -> str:
    """Remove trigger phrases from command to extract the query."""
    result = command
    for t in triggers:
        result = result.replace(t, "")
    result = re.sub(
        r'^(please|can you|could you|i want to|i want|for|search for|'
        r'search|find|play|look up|look for)\s+', '', result.strip())
    return result.strip()


# ============================================================
# NEW UTILITY FUNCTIONS (v4)
# ============================================================

def _calculate(expression: str) -> str:
    """Safely evaluate a math expression."""
    try:
        expr = expression.replace("x", "*").replace("÷", "/").replace("^", "**")
        expr = re.sub(r'[^0-9+\-*/().%\s]', '', expr)
        if not expr.strip():
            return "❌ Invalid expression. Try: calculate 5 + 3 * 2"
        result = eval(expr)
        return f"🧮 {expression} = **{result}**"
    except ZeroDivisionError:
        return "❌ Cannot divide by zero!"
    except Exception:
        return f"❌ Could not calculate: {expression}\nTry: calculate 5 + 3 * 2"


def _generate_password(length: int = 16) -> str:
    """Generate a strong random password."""
    if length < 8: length = 8
    if length > 64: length = 64
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    pwd = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*"),
    ]
    pwd += [random.choice(chars) for _ in range(length - 4)]
    random.shuffle(pwd)
    return f"🔑 Generated Password ({length} chars):\n{''.join(pwd)}"


def _get_uptime() -> str:
    """Get system uptime."""
    try:
        import psutil
        boot = datetime.datetime.fromtimestamp(psutil.boot_time())
        now = datetime.datetime.now()
        delta = now - boot
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return (f"⏱️ System Uptime: {hours}h {minutes}m {seconds}s\n"
                f"Booted: {boot.strftime('%I:%M %p, %b %d')}")
    except:
        return "❌ Could not get uptime."


def _get_quote() -> str:
    """Return a random motivational quote."""
    quotes = [
        ("The best way to predict the future is to create it.", "Abraham Lincoln"),
        ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Stay hungry, stay foolish.", "Steve Jobs"),
        ("First, solve the problem. Then, write the code.", "John Johnson"),
        ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
        ("It's not a bug — it's an undocumented feature.", "Anonymous"),
        ("The best error message is the one that never shows up.", "Thomas Fuchs"),
        ("Talk is cheap. Show me the code.", "Linus Torvalds"),
        ("Simplicity is the soul of efficiency.", "Austin Freeman"),
        ("Make it work, make it right, make it fast.", "Kent Beck"),
        ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
        ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
        ("The harder I work, the luckier I get.", "Samuel Goldwyn"),
        ("Dream big, start small, act now.", "Robin Sharma"),
    ]
    quote, author = random.choice(quotes)
    return f"💡 \"{quote}\"\n   — {author}"


def _count_text(text: str) -> str:
    """Count words, characters, and sentences in text."""
    words = len(text.split())
    chars = len(text)
    chars_no_space = len(text.replace(" ", ""))
    sentences = text.count('.') + text.count('!') + text.count('?')
    return (f"📊 Text Statistics:\n"
            f"  Words: {words}\n"
            f"  Characters: {chars} (without spaces: {chars_no_space})\n"
            f"  Sentences: {sentences}")


def _get_day_of_date(date_str: str) -> str:
    """Get the day of the week for a given date."""
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%m-%d-%Y",
                "%d %b %Y", "%B %d %Y", "%d %B %Y"):
        try:
            dt = datetime.datetime.strptime(date_str.strip(), fmt)
            return f"📅 {dt.strftime('%A, %B %d, %Y')} — It's a **{dt.strftime('%A')}**"
        except:
            continue
    return (f"❌ Could not parse date: '{date_str}'\n"
            f"Try formats: 25-12-2024, 2024-12-25, 25/12/2024")


class AssistantCore:
    """Central command router for the JEEVES desktop assistant."""

    def __init__(self, config: dict):
        self.config = config
        self.assistant_name = config.get('assistant_name', 'Jeeves')
        self.user_name = config.get('user_name', 'Boss')
        self.arduino = arduino_control.ArduinoController(config)
        self.ai = ai_module.AIModule(config)
        self.active_game = None
        self.active_game_name = ""

        # AI Permission system
        self._pending_ai_query = None    # Stores the query waiting for yes/no
        self._awaiting_ai_confirm = False  # True when waiting for yes/no

    def process_command(self, command: str) -> str:
        """Process a text command and return the response."""
        command = command.lower().strip()
        if not command:
            return "I didn't catch that. Can you say it again?"

        # ============================================================
        # AI PERMISSION CHECK — if we're waiting for yes/no
        # ============================================================
        if self._awaiting_ai_confirm:
            if command in ["yes", "y", "sure", "ok", "okay", "go ahead",
                           "yeah", "yep", "do it", "please", "haan", "ha"]:
                query = self._pending_ai_query
                self._pending_ai_query = None
                self._awaiting_ai_confirm = False
                if self.ai.is_available:
                    return self.ai.ask(query)
                return "❌ AI is not available. Please set your API key in Settings."
            elif command in ["no", "n", "nope", "nah", "cancel", "skip", "nahi"]:
                self._pending_ai_query = None
                self._awaiting_ai_confirm = False
                return "👍 Okay, I won't use AI for that. Anything else I can help with?"
            else:
                # They typed something else — treat it as new command, cancel AI prompt
                self._pending_ai_query = None
                self._awaiting_ai_confirm = False
                # Fall through to normal processing below

        # ============================================================
        # GAME MODE — if a game is active, route to it
        # ============================================================
        if self.active_game is not None:
            if command in ["quit", "exit game", "stop game", "end game",
                           "quit game", "stop"]:
                name = self.active_game_name
                self.active_game = None
                self.active_game_name = ""
                return f"🎮 Exited {name}. What would you like to do?"
            response = self.active_game.play(command)
            if not self.active_game.is_active:
                self.active_game = None
                self.active_game_name = ""
            return response

        # ============================================================
        # GREETINGS
        # ============================================================
        greet_words = ["hello", "hi", "hey", "good morning", "good afternoon",
                       "good evening", "howdy", "sup", "yo", "what's up",
                       "wassup", "hola", "namaste", "greetings", "assalam o alaikum",
                       "salam", "hi there", "hey there"]
        if command in greet_words or command.rstrip("!") in greet_words:
            hour = datetime.datetime.now().hour
            if hour < 12: g = "Good morning"
            elif hour < 17: g = "Good afternoon"
            else: g = "Good evening"
            return f"👋 {g}, {self.user_name}! How can I help you?"

        # ============================================================
        # HELP & INFO
        # ============================================================
        if command in ["help", "commands", "what can you do", "help me",
                       "show commands", "all commands", "command list"]:
            return self._get_help_text()

        if any(w in command for w in ["who are you", "about", "what are you",
                                       "introduce yourself", "your name"]):
            return (f"🤖 I'm {self.assistant_name}, your desktop assistant!\n"
                    f"I can control your PC, open apps, play games, send WhatsApp messages, "
                    f"connect to Arduino/ESP32, and answer questions with AI.\n"
                    f"Type 'help' to see all my commands!")

        # ============================================================
        # SYSTEM CONTROL
        # ============================================================
        if "battery" in command or "power status" in command:
            return system_control.get_battery_status()

        if command in ["time", "what time", "current time"] or \
           "what is the time" in command or "what's the time" in command or \
           "tell me the time" in command or "show time" in command:
            return system_control.get_time()

        if command in ["date", "today"] or "what date" in command or \
           "what day" in command or "what is the date" in command or \
           "what's the date" in command or "today's date" in command or \
           "tell me the date" in command or "show date" in command:
            return system_control.get_date()

        if "date and time" in command or "date time" in command or "datetime" in command:
            return system_control.get_date_time()

        if "recycle bin" in command or "empty trash" in command:
            return system_control.empty_recycle_bin()

        if "screenshot" in command or "screen capture" in command or \
           "capture screen" in command or "take a screenshot" in command:
            return system_control.take_screenshot(self.config)

        if "system info" in command or "sysinfo" in command or \
           "pc info" in command or "computer info" in command or \
           "system status" in command or "pc status" in command:
            return system_control.get_system_info()

        if command in ["ip", "ip address", "my ip"] or \
           "what is my ip" in command or "my ip address" in command:
            return system_control.get_ip_address()

        if command in ["lock", "lock pc", "lock screen", "lock computer"] or \
           "lock the pc" in command or "lock my pc" in command:
            return system_control.lock_pc()

        if "shutdown" in command or "shut down" in command or "power off" in command:
            if "cancel" in command or "abort" in command:
                return system_control.cancel_shutdown()
            return system_control.shutdown_pc()

        if "restart" in command or "reboot" in command:
            if "cancel" in command:
                return system_control.cancel_shutdown()
            return system_control.restart_pc()

        if "cancel shutdown" in command or "abort shutdown" in command:
            return system_control.cancel_shutdown()

        # Volume
        if "volume up" in command or "increase volume" in command or \
           "louder" in command or "turn up volume" in command or "raise volume" in command:
            return system_control.set_volume("up")

        if "volume down" in command or "decrease volume" in command or \
           "quieter" in command or "softer" in command or \
           "turn down volume" in command or "lower volume" in command:
            return system_control.set_volume("down")

        if command in ["mute", "unmute"] or "toggle mute" in command or \
           "mute volume" in command:
            return system_control.set_volume("mute")

        # Brightness
        if "brightness up" in command or "increase brightness" in command or \
           "brighter" in command:
            return system_control.set_brightness("up")

        if "brightness down" in command or "decrease brightness" in command or \
           "dimmer" in command or "dim screen" in command:
            return system_control.set_brightness("down")

        # Search folder
        if "search folder" in command or "find folder" in command:
            query = _extract_query(command, ["search folder", "find folder"])
            if query:
                return system_control.search_folder(query, self.config)
            return "Please specify a folder name. Example: 'search folder projects'"

        # Open folder / file
        if command.startswith("open folder "):
            path = command.replace("open folder ", "").strip()
            return system_control.open_folder(path) if path else "Specify a folder path."

        if command.startswith("open file "):
            path = command.replace("open file ", "").strip()
            return system_control.open_file(path) if path else "Specify a file path."

        # ============================================================
        # WHATSAPP MESSAGING (before generic browser handling)
        # ============================================================
        if ("whatsapp" in command or "watsapp" in command or "whats app" in command) and \
           ("send" in command or "message" in command or "msg" in command):
            return self._handle_whatsapp_send(command)

        if "whatsapp" in command or "watsapp" in command or "whats app" in command:
            return browser_control.open_whatsapp(self.config)

        # ============================================================
        # YOUTUBE — ONLY when user explicitly wants YouTube
        # ============================================================
        if "youtube" in command:
            if command in ["open youtube", "youtube", "go to youtube",
                           "launch youtube", "start youtube"]:
                return browser_control.open_website("youtube", self.config)

            query = _extract_query(command, [
                "on youtube", "youtube", "search youtube", "youtube search",
                "play youtube", "youtube play", "find on youtube",
                "search on youtube", "look up on youtube", "watch",
            ])
            if query:
                return browser_control.search_youtube(query, self.config)
            return browser_control.open_website("youtube", self.config)

        # ============================================================
        # GOOGLE SEARCH — ONLY when user explicitly says "google" or "search"
        # ============================================================
        if "google" in command:
            if command in ["open google", "google", "go to google"]:
                return browser_control.open_website("google", self.config)
            query = _extract_query(command, [
                "on google", "google", "search google", "google search",
                "google for", "search on google",
            ])
            if query:
                return browser_control.search_google(query, self.config)
            return browser_control.open_website("google", self.config)

        # "search <X>" / "search for <X>" → Google only
        if command.startswith("search ") or command.startswith("search for ") or \
           command.startswith("look up "):
            query = _extract_query(command, ["search for", "search", "look up"])
            if query:
                return browser_control.search_google(query, self.config)

        # ============================================================
        # BROWSER / WEBSITES / APPS
        # ============================================================
        if command in ["open chrome", "chrome", "browser", "launch chrome",
                       "start chrome", "open browser"]:
            return browser_control.open_chrome(self.config)

        if command in ["websites", "list websites", "available websites",
                       "show websites", "website list"]:
            return browser_control.get_available_websites()

        # "open <X>" → website or app
        if command.startswith("open ") or command.startswith("launch ") or \
           command.startswith("start ") or command.startswith("run "):
            app_name = re.sub(r'^(open|launch|start|run)\s+', '', command).strip()
            if app_name in browser_control.WEBSITES:
                return browser_control.open_website(app_name, self.config)
            return system_control.open_application(app_name)

        # Close app
        if command.startswith("close ") or command.startswith("kill "):
            app_name = re.sub(r'^(close|kill)\s+', '', command).strip()
            try:
                os.system(f'taskkill /f /im {app_name}.exe 2>nul')
                return f"✅ Closed {app_name}"
            except:
                return f"❌ Could not close {app_name}"

        # ============================================================
        # ARDUINO / ESP32
        # ============================================================
        if "list ports" in command or "com ports" in command or \
           "serial ports" in command or "available ports" in command:
            return self.arduino.list_ports()

        if "connect arduino" in command or "arduino connect" in command:
            port_match = re.search(r'com\d+', command, re.IGNORECASE)
            if port_match:
                return self.arduino.connect_serial(port_match.group().upper())
            return self.arduino.connect_serial()

        if "disconnect arduino" in command or "arduino disconnect" in command:
            return self.arduino.disconnect_serial()

        if command.startswith("send ") and "whatsapp" not in command:
            cmd = _extract_query(command, ["arduino send", "send to arduino", "send"])
            return self.arduino.send_serial(cmd)

        if "read arduino" in command or "arduino read" in command:
            return self.arduino.read_serial()

        if "wifi send" in command or "esp32 send" in command or "esp send" in command:
            cmd = _extract_query(command, ["wifi send", "esp32 send", "esp send"])
            return self.arduino.send_wifi(cmd)

        if "esp32 status" in command or "wifi status" in command or \
           "check esp32" in command:
            return self.arduino.check_esp32_status()

        if "arduino status" in command or "connection status" in command or \
           "device status" in command:
            return self.arduino.get_status()

        # Quick Arduino
        if "led on" in command or "turn on led" in command or "light on" in command:
            return self.arduino.send_serial("LED_ON")
        if "led off" in command or "turn off led" in command or "light off" in command:
            return self.arduino.send_serial("LED_OFF")
        if "motor on" in command or "start motor" in command:
            return self.arduino.send_serial("MOTOR_ON")
        if "motor off" in command or "stop motor" in command:
            return self.arduino.send_serial("MOTOR_OFF")

        # ============================================================
        # GAMES & ENTERTAINMENT
        # ============================================================
        if command in ["games", "list games", "play games", "entertainment",
                       "play", "game list", "show games"]:
            return games.get_games_list()

        game_map = {
            ("number guess", "guess number", "guessing game"): ("NumberGuessingGame", "Number Guessing Game"),
            ("quiz", "trivia", "play quiz", "play trivia"): ("TriviaQuiz", "Trivia Quiz"),
            ("rps", "rock paper scissors"): ("RockPaperScissors", "Rock Paper Scissors"),
            ("tictactoe", "tic tac toe", "tic-tac-toe"): ("TicTacToe", "Tic-Tac-Toe"),
            ("scramble", "word scramble"): ("WordScramble", "Word Scramble"),
            ("math", "math challenge", "math quiz"): ("MathChallenge", "Math Challenge"),
            ("hangman", "hang man"): ("Hangman", "Hangman"),
        }
        for triggers, (class_name, display_name) in game_map.items():
            if any(t in command for t in triggers):
                self.active_game = getattr(games, class_name)()
                self.active_game_name = display_name
                return self.active_game.start()

        if "flip coin" in command or "coin flip" in command or \
           "toss coin" in command or "heads or tails" in command:
            return games.coin_flip()

        if "roll dice" in command or "dice roll" in command or \
           "throw dice" in command or "roll a dice" in command:
            return games.dice_roll()

        if "joke" in command or "tell joke" in command or \
           "tell me a joke" in command or "something funny" in command or \
           "make me laugh" in command:
            return games.tell_joke()

        if "random number" in command or "give me a number" in command:
            return games.random_number()

        if "8ball" in command or "magic ball" in command or "eight ball" in command:
            return games.magic_8ball()

        # ============================================================
        # AI — explicit commands (always allowed without permission)
        # ============================================================
        if "ai status" in command or "gemini status" in command or "check ai" in command:
            return self.ai.get_status()

        if "clear history" in command or "new conversation" in command or \
           "reset ai" in command or "clear chat history" in command:
            return self.ai.clear_history()

        if command.startswith("set api key ") or command.startswith("api key "):
            key = _extract_query(command, ["set api key", "api key"])
            return self.ai.set_api_key(key)

        # Explicit AI commands (user intentionally asks AI → no permission needed)
        if command.startswith("ask "):
            question = command[4:].strip()
            if self.ai.is_available:
                return self.ai.ask(question)
            return "❌ AI is not available. Please set your API key in Settings."

        if "research " in command and command.startswith("research"):
            topic = _extract_query(command, ["research", "research about", "research on"])
            if self.ai.is_available:
                return self.ai.research(topic)
            return "❌ AI is not available. Please set your API key in Settings."

        if "generate code" in command or "write code" in command:
            desc = _extract_query(command, ["generate code", "write code", "code for"])
            if self.ai.is_available:
                return self.ai.generate_code(desc)
            return "❌ AI is not available. Please set your API key in Settings."

        if command.startswith("summarize ") or "summarize " in command:
            text = _extract_query(command, ["summarize", "summarize this"])
            if self.ai.is_available:
                return self.ai.summarize(text)
            return "❌ AI is not available. Please set your API key in Settings."

        # ============================================================
        # NEW v4 FEATURES
        # ============================================================

        # Calculator
        if "calculate" in command or "calc " in command or "math " in command:
            expr = _extract_query(command, ["calculate", "calc", "math", "evaluate",
                                             "what is", "whats", "how much is"])
            return _calculate(expr) if expr else "🧮 Try: calculate 5 + 3 * 2"

        # Password generator
        if "password" in command or "generate password" in command or \
           "random password" in command:
            length = 16
            nums = re.findall(r'\d+', command)
            if nums:
                length = int(nums[0])
            return _generate_password(length)

        # System uptime
        if "uptime" in command or "how long" in command and "running" in command:
            return _get_uptime()

        # Motivational quote
        if "quote" in command or "motivat" in command or "inspire" in command:
            return _get_quote()

        # Word/character count
        if "count" in command and ("word" in command or "character" in command or "text" in command):
            text = _extract_query(command, ["count words", "count characters",
                                             "word count", "character count",
                                             "count text", "count"])
            return _count_text(text) if text else "📊 Try: count words Hello world, how are you?"

        # Day of date
        if "day of" in command or "what day was" in command or "what day is" in command:
            date_str = _extract_query(command, ["what day was", "what day is",
                                                 "day of", "which day"])
            return _get_day_of_date(date_str) if date_str else "📅 Try: what day is 25-12-2024"

        # Clipboard copy
        if "copy" in command and ("clipboard" in command or "to clipboard" in command):
            text_to_copy = _extract_query(command, ["copy to clipboard", "copy clipboard", "copy"])
            if text_to_copy:
                try:
                    import pyperclip
                    pyperclip.copy(text_to_copy)
                    return f"📋 Copied to clipboard: \"{text_to_copy[:50]}…\"" if len(text_to_copy) > 50 else f"📋 Copied to clipboard: \"{text_to_copy}\""
                except:
                    return "❌ Clipboard operation failed."
            return "📋 Try: copy to clipboard Hello World"

        # System platform info
        if "os info" in command or "os version" in command or "windows version" in command:
            return (f"💻 Platform: {platform.system()} {platform.release()}\n"
                    f"Version: {platform.version()}\n"
                    f"Machine: {platform.machine()}\n"
                    f"Processor: {platform.processor()}")

        # ============================================================
        # FAREWELL
        # ============================================================
        if command in ["bye", "goodbye", "see you", "exit", "quit", "close",
                       "see you later", "goodnight", "good night", "go to sleep"]:
            return f"👋 Goodbye, {self.user_name}! Have a great day! 😊"

        if "thanks" in command or "thank you" in command or "thx" in command:
            return f"😊 You're welcome, {self.user_name}! Always happy to help!"

        # ============================================================
        # CONVERSATIONAL
        # ============================================================
        if "how are you" in command:
            return f"😊 I'm doing great, {self.user_name}! Ready to help. What do you need?"

        if "what can you do" in command or "your capabilities" in command:
            return self._get_help_text()

        if "reminder" in command or "remind me" in command:
            return "⏰ Reminder feature coming soon! For now, try setting a Windows alarm."

        if "timer" in command or "set timer" in command or "countdown" in command:
            return "⏱️ Timer feature coming soon! Try: 'search online timer'"

        if "note" in command and ("take" in command or "make" in command or "write" in command):
            return "📝 Try opening Notepad: 'open notepad'"

        # "play <something>" without "youtube" → search YouTube
        if command.startswith("play "):
            query = _extract_query(command, ["play music", "play song", "play video", "play"])
            if query:
                return browser_control.search_youtube(query, self.config)

        # ============================================================
        # FALLBACK — Ask permission to use AI, or say not trained
        # ============================================================
        if self.ai.is_available:
            self._pending_ai_query = command
            self._awaiting_ai_confirm = True
            return (f"🤖 I don't have a built-in command for that.\n"
                    f"Shall I use AI (Gemini API) to answer: \"{command}\"?\n"
                    f"Type **yes** or **no**.")
        else:
            return (f"🤷 I'm not trained to answer: \"{command}\"\n\n"
                    f"Here's what I can do:\n"
                    f"• Type 'help' to see all available commands\n"
                    f"• Type 'search <query>' to Google something\n"
                    f"• Set up a Gemini API key in Settings to unlock AI answers")

    # ============================================================
    # WHATSAPP SEND HELPER
    # ============================================================
    def _handle_whatsapp_send(self, command: str) -> str:
        """Parse WhatsApp send command and extract phone + message."""
        cleaned = command
        for word in ["send", "whatsapp", "watsapp", "whats app", "message",
                     "msg", "to", "on", "a", "please"]:
            cleaned = cleaned.replace(word, "")
        cleaned = cleaned.strip()

        if not cleaned:
            return ("📱 **WhatsApp Message — How to use:**\n"
                    "  send whatsapp <phone_number> <message>\n\n"
                    "**Examples:**\n"
                    "  send whatsapp 923001234567 Hello how are you?\n"
                    "  send whatsapp +923001234567 Meeting at 5pm\n\n"
                    "💡 Use country code (92 for PK, 1 for US)")

        parts = cleaned.split(None, 1)
        if len(parts) < 2:
            return ("❌ Please provide both phone number AND message.\n"
                    "Format: send whatsapp <phone_number> <message>\n"
                    "Example: send whatsapp 923001234567 Hello!")

        phone = parts[0]
        message = parts[1]
        return browser_control.send_whatsapp_message(phone, message, self.config)

    # ============================================================
    # UTILITY
    # ============================================================
    def get_greeting(self) -> str:
        hour = datetime.datetime.now().hour
        if hour < 12: g = "Good morning"
        elif hour < 17: g = "Good afternoon"
        else: g = "Good evening"
        return (f"👋 {g}, {self.user_name}! "
                f"I'm {self.assistant_name}, your AI desktop assistant.\n"
                f"Type 'help' to see what I can do, or just ask me anything!")

    def cleanup(self) -> None:
        self.arduino.cleanup()

    def _get_help_text(self) -> str:
        return """📋 **JEEVES v4.0 — Command Reference**

💻 **System:**
  battery | time | date | screenshot
  system info | ip address | lock pc
  empty recycle bin | shutdown | restart
  volume up/down/mute | brightness up/down
  uptime | os info

📂 **Files & Apps:**
  open <app>  (notepad, calculator, vs code…)
  open folder <path> | search folder <name>
  close <app> | open file <path>

🌐 **Web & Search:**
  search <anything>  — Google search
  <anything> on youtube  — YouTube search
  play <song/video>  — YouTube search
  open youtube/chrome/gmail/whatsapp

💬 **WhatsApp:**
  open whatsapp — Opens WhatsApp Web
  send whatsapp <phone> <message>

🔌 **Arduino / ESP32:**
  list ports | connect arduino [COMx]
  send <cmd> | led on/off | motor on/off
  wifi send <cmd> | esp32 status

🤖 **AI (needs API key + permission):**
  ask <question> | research <topic>
  generate code <desc> | summarize <text>

🧰 **Utilities (NEW!):**
  calculate <expression>  — Math calculator
  generate password [length]  — Random password
  uptime  — System boot time
  quote / motivate  — Inspirational quote
  count words <text>  — Word/char counter
  what day is <date>  — Day of week
  copy to clipboard <text>  — Copy text
  os info  — Platform details

🎮 **Games:**
  games | play quiz/rps/tictactoe/hangman
  play number guess/scramble/math
  flip coin | roll dice | joke | 8ball

⚙️ **Other:**  help | about | bye"""

