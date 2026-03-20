# ============================================================
# app_gui.py — CustomTkinter GUI v4 (Hackathon Edition)
# ============================================================
# LAYOUT: Sidebar | Big Center Visualizer | Right Chat Panel
# FIXES: TTS now speaks ALL responses (truncated if too long)
# NEW:   Gradient-style header, glow mic button, animated title
# ============================================================

import customtkinter as ctk
import threading
import json
import os
import datetime
import time as _time

from core.assistant_core import AssistantCore
from core.voice_module import speak, listen, reset_engine, get_available_voices
from gui.voice_visualizer import VoiceVisualizer

# ============================================================
# THEME
# ============================================================
COLORS = {
    "bg_dark": "#0A0A0F",           # Deep dark navy-black
    "bg_medium": "#12121A",         # Slightly lighter
    "bg_light": "#1A1A2E",          # Card backgrounds
    "bg_card": "#16213E",           # Elevated panels
    "accent": "#FF6600",            # Primary orange
    "accent_hover": "#FF8533",
    "accent_dark": "#CC5200",
    "accent_glow": "#FF660040",     # Transparent glow
    "text_primary": "#E8E8E8",
    "text_secondary": "#A0A0B0",
    "text_muted": "#5A5A6E",
    "success": "#00E676",           # Bright green
    "error": "#FF4444",
    "border": "#2A2A3E",
    "listening": "#00E5FF",         # Bright cyan
    "header_bg": "#0F0F1A",        # Header gradient base
    "sidebar_bg": "#0E0E18",
    "glow_orange": "#FF660025",
}

FONTS = {
    "title": ("Segoe UI", 20, "bold"),
    "subtitle": ("Segoe UI", 10),
    "body": ("Segoe UI", 12),
    "body_bold": ("Segoe UI", 12, "bold"),
    "small": ("Segoe UI", 10),
    "chat": ("Cascadia Code", 11),     # Modern monospace
    "chat_fallback": ("Consolas", 11), # Fallback
    "chat_name": ("Segoe UI", 11, "bold"),
    "button": ("Segoe UI", 11, "bold"),
    "header_btn": ("Segoe UI", 10),
    "status": ("Segoe UI", 9),
    "viz_label": ("Segoe UI", 12, "bold"),
    "mic_btn": ("Segoe UI", 11, "bold"),
    "section_title": ("Segoe UI", 11, "bold"),
}

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 620
SIDEBAR_WIDTH = 160
VIZ_PANEL_WIDTH = 290
VISUALIZER_SIZE = 200
MAX_SPEAK_LENGTH = 500  # Speak up to this many characters (truncate rest)

SIDEBAR_BUTTONS = [
    ("🔋  Battery", "battery"),
    ("🕐  Time", "time"),
    ("📅  Date", "date"),
    ("📸  Screenshot", "screenshot"),
    ("💻  System Info", "system info"),
    ("⏱️  Uptime", "uptime"),
    ("─────────", None),
    ("🌐  Chrome", "open chrome"),
    ("📺  YouTube", "open youtube"),
    ("💬  WhatsApp", "open whatsapp"),
    ("📧  Gmail", "open gmail"),
    ("─────────", None),
    ("🔌  Arduino", "arduino status"),
    ("🤖  AI Status", "ai status"),
    ("─────────", None),
    ("🎮  Games", "games"),
    ("😂  Joke", "tell joke"),
    ("🔑  Password", "generate password"),
    ("📋  Help", "help"),
]


class JeevesGUI:
    """Main GUI — Hackathon Edition with fixed TTS and enhanced visuals."""

    def __init__(self, config: dict):
        self.config = config
        self.core = AssistantCore(config)
        self.is_listening = False
        self.is_speaking = False

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title(f"⚡ {config.get('assistant_name', 'Jeeves')} — AI Desktop Assistant")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(900, 520)
        self.root.configure(fg_color=COLORS["bg_dark"])

        # Center on screen
        self.root.update_idletasks()
        sx = (self.root.winfo_screenwidth() - WINDOW_WIDTH) // 2
        sy = (self.root.winfo_screenheight() - WINDOW_HEIGHT) // 2
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{sx}+{sy}")

        self._build_header()
        self._build_body()
        self._build_status_bar()

        if config.get('greeting_enabled', True):
            greeting = self.core.get_greeting()
            self._add_bot_message(greeting)
            # Speak greeting in background
            threading.Thread(target=lambda: self._speak_text(greeting), daemon=True).start()

        self.root.bind('<Return>', lambda e: self._on_send())
        self.root.bind('<Control-m>', lambda e: self._on_mic_click())
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ========================================================
    # SPEAK HELPER — used everywhere to ensure TTS works
    # ========================================================
    def _speak_text(self, text: str):
        """
        Speak text with proper visualizer state management.
        Truncates very long text so TTS doesn't take forever.
        """
        if not text or text.startswith("[Error]"):
            return
        # Strip emojis/special chars that TTS can't pronounce well
        clean = text
        for ch in "📋🔋🕐📅📸💻🌐📺💬📧🔌🤖🎮😂🔑⚡👋😊✅❌🤔🤷⏳💡🎭📱🔆🔅⏰⏱️📝":
            clean = clean.replace(ch, "")
        clean = clean.strip()
        if not clean:
            return

        # Truncate for long responses
        if len(clean) > MAX_SPEAK_LENGTH:
            clean = clean[:MAX_SPEAK_LENGTH] + "... and more."

        try:
            self.root.after(0, lambda: self._set_viz_state("speaking"))
            speak(clean, self.config)
        except Exception as e:
            print(f"[TTS Error] {e}")
        finally:
            self.root.after(0, lambda: self._set_viz_state("idle"))

    # ========================================================
    # HEADER
    # ========================================================
    def _build_header(self):
        header = ctk.CTkFrame(self.root, height=56, fg_color=COLORS["header_bg"], corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Title with accent
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=15)

        # Glowing icon
        ctk.CTkLabel(
            title_frame, text="⚡", font=("Segoe UI", 24),
            text_color=COLORS["accent"]
        ).pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text=self.config.get('assistant_name', 'JEEVES').upper(),
            font=("Segoe UI", 22, "bold"), text_color=COLORS["accent"]
        ).pack(side="left", padx=(4, 0))

        ctk.CTkLabel(
            title_frame, text="AI Assistant",
            font=("Segoe UI", 11), text_color=COLORS["text_muted"]
        ).pack(side="left", padx=(10, 0), pady=(6, 0))

        # Version badge
        ctk.CTkLabel(
            title_frame, text="v4.0",
            font=("Segoe UI", 8, "bold"), text_color=COLORS["bg_dark"],
            fg_color=COLORS["accent"], corner_radius=6, width=36, height=18
        ).pack(side="left", padx=(8, 0), pady=(4, 0))

        # Header buttons
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right", padx=12)

        for text, cmd in [("⚙️ Settings", self._open_settings), ("🗑️ Clear", self._clear_chat)]:
            ctk.CTkButton(
                btn_frame, text=text, font=FONTS["header_btn"],
                width=90, height=30,
                fg_color=COLORS["bg_light"], hover_color=COLORS["accent_dark"],
                text_color=COLORS["text_secondary"], corner_radius=8,
                border_width=1, border_color=COLORS["border"],
                command=cmd
            ).pack(side="right", padx=3)

    # ========================================================
    # BODY: 3 panels
    # ========================================================
    def _build_body(self):
        body = ctk.CTkFrame(self.root, fg_color=COLORS["bg_dark"])
        body.pack(fill="both", expand=True)
        self._build_sidebar(body)
        self._build_viz_panel(body)
        self._build_chat_panel(body)

    def _build_sidebar(self, parent):
        sidebar = ctk.CTkFrame(parent, width=SIDEBAR_WIDTH, fg_color=COLORS["sidebar_bg"], corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(
            sidebar, text="⚡ Quick Actions",
            font=FONTS["section_title"], text_color=COLORS["accent"]
        ).pack(pady=(12, 6))

        scroll = ctk.CTkScrollableFrame(
            sidebar, fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["accent"]
        )
        scroll.pack(fill="both", expand=True, padx=4)

        for label, command in SIDEBAR_BUTTONS:
            if command is None:
                ctk.CTkFrame(scroll, height=1, fg_color=COLORS["border"]).pack(fill="x", pady=5, padx=8)
            else:
                ctk.CTkButton(
                    scroll, text=label, font=FONTS["small"],
                    height=30, fg_color="transparent",
                    hover_color=COLORS["bg_card"],
                    text_color=COLORS["text_secondary"],
                    anchor="w", corner_radius=8,
                    command=lambda c=command: self._execute_command(c)
                ).pack(fill="x", pady=1, padx=2)

    def _build_viz_panel(self, parent):
        viz_panel = ctk.CTkFrame(parent, width=VIZ_PANEL_WIDTH, fg_color=COLORS["bg_dark"], corner_radius=0)
        viz_panel.pack(side="left", fill="y")
        viz_panel.pack_propagate(False)

        # Spacer
        ctk.CTkFrame(viz_panel, fg_color="transparent", height=15).pack()

        # Orb
        self.visualizer = VoiceVisualizer(viz_panel, size=VISUALIZER_SIZE)
        self.visualizer.pack(pady=(20, 6))

        # State label
        self.state_label = ctk.CTkLabel(
            viz_panel, text="● READY",
            font=FONTS["viz_label"], text_color=COLORS["success"]
        )
        self.state_label.pack(pady=(0, 10))

        # Glowing mic button
        self.mic_btn = ctk.CTkButton(
            viz_panel, text="🎤  Tap to Speak",
            width=170, height=46, font=FONTS["mic_btn"],
            fg_color=COLORS["bg_card"], hover_color=COLORS["accent"],
            text_color=COLORS["text_primary"],
            corner_radius=23, border_width=2,
            border_color=COLORS["accent"],
            command=self._on_mic_click
        )
        self.mic_btn.pack(pady=(6, 0))

        ctk.CTkLabel(
            viz_panel, text="or press Ctrl + M",
            font=("Segoe UI", 9), text_color=COLORS["text_muted"]
        ).pack(pady=(6, 0))

        # Quick info at bottom of viz panel
        info_frame = ctk.CTkFrame(viz_panel, fg_color=COLORS["bg_light"], corner_radius=10)
        info_frame.pack(side="bottom", fill="x", padx=12, pady=(0, 12))

        self.clock_label = ctk.CTkLabel(
            info_frame, text="", font=("Segoe UI", 10),
            text_color=COLORS["text_muted"]
        )
        self.clock_label.pack(pady=6)
        self._update_clock()

    def _update_clock(self):
        """Update the live clock display in the visualizer panel."""
        now = datetime.datetime.now()
        self.clock_label.configure(text=now.strftime("%I:%M:%S %p  │  %b %d, %Y"))
        self.root.after(1000, self._update_clock)

    def _build_chat_panel(self, parent):
        chat_frame = ctk.CTkFrame(parent, fg_color=COLORS["bg_medium"], corner_radius=0)
        chat_frame.pack(side="right", fill="both", expand=True)

        # Chat label with online indicator
        header = ctk.CTkFrame(chat_frame, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(8, 2))

        ctk.CTkLabel(
            header, text="💬 Command Log",
            font=FONTS["section_title"], text_color=COLORS["accent"],
            anchor="w"
        ).pack(side="left")

        self.msg_count_label = ctk.CTkLabel(
            header, text="0 messages",
            font=("Segoe UI", 9), text_color=COLORS["text_muted"]
        )
        self.msg_count_label.pack(side="right")
        self._msg_count = 0

        # Chat display
        self.chat_display = ctk.CTkTextbox(
            chat_frame, fg_color=COLORS["bg_dark"],
            text_color=COLORS["text_primary"],
            font=FONTS["chat"], wrap="word",
            state="disabled", corner_radius=10,
            border_width=1, border_color=COLORS["border"],
            scrollbar_button_color=COLORS["accent"],
            scrollbar_button_hover_color=COLORS["accent_hover"]
        )
        self.chat_display.pack(fill="both", expand=True, padx=8, pady=(2, 4))

        # Tags
        self.chat_display.tag_config("user_name", foreground=COLORS["accent"])
        self.chat_display.tag_config("bot_name", foreground=COLORS["success"])
        self.chat_display.tag_config("user_msg", foreground=COLORS["text_primary"])
        self.chat_display.tag_config("bot_msg", foreground=COLORS["text_secondary"])
        self.chat_display.tag_config("system", foreground=COLORS["text_muted"])
        self.chat_display.tag_config("error", foreground=COLORS["error"])
        self.chat_display.tag_config("thinking", foreground=COLORS["listening"])

        self._build_input_bar(chat_frame)

    def _build_input_bar(self, parent):
        bar = ctk.CTkFrame(parent, height=54, fg_color=COLORS["bg_light"],
                           corner_radius=14, border_width=1, border_color=COLORS["border"])
        bar.pack(fill="x", padx=8, pady=(0, 8))
        bar.pack_propagate(False)

        self.input_field = ctk.CTkEntry(
            bar, placeholder_text="Type a command or ask a question…",
            font=FONTS["body"],
            fg_color=COLORS["bg_medium"], text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_muted"],
            border_width=0, corner_radius=10, height=38
        )
        self.input_field.pack(side="left", fill="x", expand=True, padx=(8, 4), pady=8)

        self.send_btn = ctk.CTkButton(
            bar, text="Send ➤", width=85, height=38,
            font=FONTS["button"],
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            text_color="white", corner_radius=10,
            command=self._on_send
        )
        self.send_btn.pack(side="right", padx=(4, 8), pady=8)

    # ========================================================
    # STATUS BAR
    # ========================================================
    def _build_status_bar(self):
        status = ctk.CTkFrame(self.root, height=28, fg_color=COLORS["header_bg"], corner_radius=0)
        status.pack(fill="x", side="bottom")
        status.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            status, text="✨ Ready — Type 'help' for commands",
            font=FONTS["status"], text_color=COLORS["text_muted"]
        )
        self.status_label.pack(side="left", padx=12)

        self.arduino_indicator = ctk.CTkLabel(
            status, text="🔌 Arduino: —",
            font=FONTS["status"], text_color=COLORS["text_muted"]
        )
        self.arduino_indicator.pack(side="right", padx=12)

        self.ai_indicator = ctk.CTkLabel(
            status, text="🤖 AI: —",
            font=FONTS["status"], text_color=COLORS["text_muted"]
        )
        self.ai_indicator.pack(side="right", padx=4)

        self._update_indicators()

    # ========================================================
    # CHAT METHODS
    # ========================================================
    def _add_user_message(self, text: str):
        self.chat_display.configure(state="normal")
        ts = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.insert("end", f"\n[{ts}] ", "system")
        name = self.config.get('user_name', 'You')
        self.chat_display.insert("end", f"▶ {name}: ", "user_name")
        self.chat_display.insert("end", f"{text}\n", "user_msg")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
        self._msg_count += 1
        self.msg_count_label.configure(text=f"{self._msg_count} messages")

    def _add_bot_message(self, text: str):
        self.chat_display.configure(state="normal")
        ts = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.insert("end", f"\n[{ts}] ", "system")
        name = self.config.get('assistant_name', 'Jeeves')
        self.chat_display.insert("end", f"◆ {name}: ", "bot_name")
        self.chat_display.insert("end", f"{text}\n", "bot_msg")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
        self._msg_count += 1
        self.msg_count_label.configure(text=f"{self._msg_count} messages")

    def _add_system_message(self, text: str):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n  ℹ️ {text}\n", "system")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def _add_thinking(self):
        self.chat_display.configure(state="normal")
        name = self.config.get('assistant_name', 'Jeeves')
        self.chat_display.insert("end", f"\n  ⏳ {name} is thinking…\n", "thinking")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def _remove_thinking(self):
        self.chat_display.configure(state="normal")
        content = self.chat_display.get("1.0", "end")
        name = self.config.get('assistant_name', 'Jeeves')
        marker = f"  ⏳ {name} is thinking…\n"
        if marker in content:
            idx = content.rfind(marker)
            if idx >= 0:
                lines_before = content[:idx].count('\n')
                try:
                    self.chat_display.delete(f"{lines_before + 1}.0", f"{lines_before + 2}.0")
                except:
                    pass
        self.chat_display.configure(state="disabled")

    def _clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self._msg_count = 0
        self.msg_count_label.configure(text="0 messages")
        self._add_system_message("Chat cleared.")

    # ========================================================
    # VISUALIZER STATE
    # ========================================================
    def _set_viz_state(self, state: str):
        self.visualizer.set_state(state)
        if state == "idle":
            self.state_label.configure(text="● READY", text_color=COLORS["success"])
        elif state == "listening":
            self.state_label.configure(text="● LISTENING…", text_color=COLORS["listening"])
        elif state == "speaking":
            self.state_label.configure(text="● SPEAKING…", text_color=COLORS["accent"])

    # ========================================================
    # COMMAND EXECUTION (TTS FIX: always speaks now)
    # ========================================================
    def _execute_command(self, command: str):
        if not command.strip():
            return

        self._add_user_message(command)
        self._add_thinking()
        self.status_label.configure(text=f"⚡ Processing: {command[:40]}…")
        self._set_viz_state("speaking")
        self.root.update()

        def process():
            try:
                response = self.core.process_command(command)
                self.root.after(0, self._remove_thinking)
                self.root.after(10, lambda: self._add_bot_message(response))

                # === TTS FIX: Always speak the response! ===
                # (runs in this same background thread so GUI stays responsive)
                self._speak_text(response)

                if command.lower() in ["bye", "goodbye", "exit", "quit", "close"]:
                    self.root.after(2000, self._on_close)

            except Exception as e:
                self.root.after(0, self._remove_thinking)
                self.root.after(10, lambda: self._add_bot_message(f"❌ Error: {e}"))
            finally:
                self.root.after(0, lambda: self._set_viz_state("idle"))
                self.root.after(0, lambda: self.status_label.configure(
                    text="✨ Ready — Type 'help' for commands"))
                self.root.after(0, self._update_indicators)

        threading.Thread(target=process, daemon=True).start()

    def _on_send(self):
        cmd = self.input_field.get().strip()
        if cmd:
            self.input_field.delete(0, "end")
            self._execute_command(cmd)

    def _on_mic_click(self):
        if self.is_listening:
            return
        self.is_listening = True
        self.mic_btn.configure(fg_color=COLORS["listening"], text="🔴 Listening…",
                               border_color=COLORS["listening"])
        self._set_viz_state("listening")
        self.status_label.configure(text="🎤 Listening… Speak now!")
        self.root.update()

        def voice_thread():
            try:
                self.root.after(0, lambda: self._add_system_message("🎤 Listening… Speak now!"))
                text = listen()
                if text.startswith("[Error]"):
                    self.root.after(0, lambda: self._add_system_message(text))
                else:
                    self.root.after(0, lambda: self._execute_command(text))
            except Exception as e:
                self.root.after(0, lambda: self._add_system_message(f"Voice error: {e}"))
            finally:
                self.is_listening = False
                self.root.after(0, lambda: self.mic_btn.configure(
                    fg_color=COLORS["bg_card"], text="🎤  Tap to Speak",
                    border_color=COLORS["accent"]))
                self.root.after(0, lambda: self._set_viz_state("idle"))
                self.root.after(0, lambda: self.status_label.configure(
                    text="✨ Ready — Type 'help' for commands"))

        threading.Thread(target=voice_thread, daemon=True).start()

    # ========================================================
    # SETTINGS
    # ========================================================
    def _open_settings(self):
        settings = ctk.CTkToplevel(self.root)
        settings.title("⚙️ Settings")
        settings.geometry("500x600")
        settings.configure(fg_color=COLORS["bg_dark"])
        settings.transient(self.root)
        settings.grab_set()

        ctk.CTkLabel(settings, text="⚙️ Settings", font=FONTS["title"],
                     text_color=COLORS["accent"]).pack(pady=(15, 10))

        scroll = ctk.CTkScrollableFrame(settings, fg_color=COLORS["bg_medium"], corner_radius=10)
        scroll.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        fields = [
            ("User Name", "user_name", self.config.get('user_name', 'Boss'), None),
            ("Assistant Name", "assistant_name", self.config.get('assistant_name', 'Jeeves'), None),
            ("Gemini API Key", "gemini_api_key", self.config.get('gemini_api_key', ''), "*"),
            ("Arduino COM Port", "arduino_port", self.config.get('arduino_port', 'COM3'), None),
            ("Baud Rate", "arduino_baud_rate", str(self.config.get('arduino_baud_rate', 9600)), None),
            ("ESP32 IP", "esp32_ip", self.config.get('esp32_ip', '192.168.1.100'), None),
            ("Voice Speed", "voice_rate", str(self.config.get('voice_rate', 180)), None),
            ("Voice Index (0=M, 1=F)", "voice_index", str(self.config.get('voice_index', 0)), None),
            ("Chrome Path", "browser_path", self.config.get('browser_path', ''), None),
        ]
        for label, key, default, show in fields:
            self._setting_field(scroll, label, key, default, show)

        ctk.CTkButton(
            settings, text="💾 Save Settings", font=FONTS["button"],
            height=40, fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            corner_radius=10, command=lambda: self._save_settings(settings)
        ).pack(pady=(0, 12), padx=12, fill="x")

    def _setting_field(self, parent, label, key, default, show=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=4, padx=4)
        ctk.CTkLabel(frame, text=label, font=FONTS["small"],
                     text_color=COLORS["text_secondary"]).pack(anchor="w")
        kw = {"font": FONTS["body"], "fg_color": COLORS["bg_light"],
              "text_color": COLORS["text_primary"], "border_width": 1,
              "border_color": COLORS["border"], "corner_radius": 8, "height": 34}
        if show:
            kw["show"] = show
        entry = ctk.CTkEntry(frame, **kw)
        entry.insert(0, default)
        entry.pack(fill="x", pady=(2, 0))
        if not hasattr(self, '_setting_entries'):
            self._setting_entries = {}
        self._setting_entries[key] = entry

    def _save_settings(self, win):
        try:
            for key, entry in self._setting_entries.items():
                val = entry.get().strip()
                if key in ['voice_rate', 'voice_index', 'arduino_baud_rate', 'esp32_port']:
                    try: val = int(val)
                    except: pass
                self.config[key] = val
            config_path = os.path.normpath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json'))
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            self.core = AssistantCore(self.config)
            reset_engine()
            self._update_indicators()
            self.root.title(f"⚡ {self.config.get('assistant_name', 'Jeeves')} — AI Desktop Assistant")
            self._add_system_message("✅ Settings saved!")
            win.destroy()
        except Exception as e:
            self._add_system_message(f"❌ Error saving: {e}")

    # ========================================================
    # UTILITY
    # ========================================================
    def _update_indicators(self):
        if self.core.arduino.is_serial_connected:
            self.arduino_indicator.configure(
                text=f"🔌 Arduino: ✅ {self.core.arduino.serial_port}",
                text_color=COLORS["success"])
        else:
            self.arduino_indicator.configure(text="🔌 Arduino: —", text_color=COLORS["text_muted"])
        if self.core.ai.is_available:
            self.ai_indicator.configure(text="🤖 AI: ✅", text_color=COLORS["success"])
        elif self.core.ai.api_key:
            self.ai_indicator.configure(text="🤖 AI: ⚠️", text_color=COLORS["accent"])
        else:
            self.ai_indicator.configure(text="🤖 AI: —", text_color=COLORS["text_muted"])

    def _on_close(self):
        try: self.visualizer.destroy_animation()
        except: pass
        try: self.core.cleanup()
        except: pass
        self.root.destroy()

    def run(self):
        self.input_field.focus_set()
        self.root.mainloop()
