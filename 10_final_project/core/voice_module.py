# ============================================================
# voice_module.py — Speech Recognition & Text-to-Speech
# ============================================================
# This module handles ALL voice-related operations:
#   - speak(text) : Converts text to speech using pyttsx3 (OFFLINE)
#   - listen()    : Captures voice from microphone and converts to text
#
# HOW TO CUSTOMIZE:
#   - Change voice speed  : Edit "voice_rate" in config.json (default: 180)
#   - Change voice volume : Edit "voice_volume" in config.json (0.0 to 1.0)
#   - Change voice type   : Edit "voice_index" in config.json
#       voice_index 0 = Male voice (David on Windows)
#       voice_index 1 = Female voice (Zira on Windows)
#   - To see all available voices, run: python -c "import pyttsx3; e=pyttsx3.init(); [print(i,v.id) for i,v in enumerate(e.getProperty('voices'))]"
# ============================================================

import pyttsx3                 # Offline text-to-speech engine
import speech_recognition as sr  # Microphone input & speech-to-text
import json
import os
import threading

# ============================================================
# GLOBAL: TTS engine instance (created once, reused)
# ============================================================
_engine = None
_engine_lock = threading.Lock()


def _get_engine(config: dict) -> pyttsx3.Engine:
    """
    Get or create the pyttsx3 engine with settings from config.
    Uses a lock to avoid threading issues with pyttsx3.
    
    Args:
        config (dict): Configuration dictionary from config.json
    
    Returns:
        pyttsx3.Engine: Configured TTS engine
    """
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        # --- Set voice speed (words per minute) ---
        _engine.setProperty('rate', config.get('voice_rate', 180))
        # --- Set volume (0.0 = silent, 1.0 = max) ---
        _engine.setProperty('volume', config.get('voice_volume', 1.0))
        # --- Set voice type (male/female) ---
        voices = _engine.getProperty('voices')
        voice_index = config.get('voice_index', 0)
        if voice_index < len(voices):
            _engine.setProperty('voice', voices[voice_index].id)
    return _engine


def speak(text: str, config: dict) -> None:
    """
    Convert text to speech and play it through speakers.
    This works COMPLETELY OFFLINE — no internet needed.
    
    Args:
        text (str): The text to speak out loud
        config (dict): Configuration dictionary from config.json
    
    Example:
        speak("Hello Boss, how can I help you?", config)
    """
    with _engine_lock:
        try:
            engine = _get_engine(config)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            # If TTS fails, we just print — don't crash the app
            print(f"[Voice Error] Could not speak: {e}")


def listen(timeout: int = 5, phrase_time_limit: int = 10) -> str:
    """
    Listen to the microphone and convert speech to text.
    
    Uses Google's free Speech Recognition API (needs internet).
    If offline, returns an error message.
    
    Args:
        timeout (int): Max seconds to wait for speech to START (default: 5)
        phrase_time_limit (int): Max seconds the phrase can be (default: 10)
    
    Returns:
        str: Recognized text (lowercase) or error message starting with "[Error]"
    
    Example:
        text = listen()
        if not text.startswith("[Error]"):
            process_command(text)
    """
    # --- Create recognizer and microphone instances ---
    recognizer = sr.Recognizer()
    
    # --- Adjust for ambient noise and listen ---
    try:
        with sr.Microphone() as source:
            # Calibrate for 1 second of ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Listen for audio input
            audio = recognizer.listen(
                source, 
                timeout=timeout, 
                phrase_time_limit=phrase_time_limit
            )
        
        # --- Convert speech to text using Google's free API ---
        text = recognizer.recognize_google(audio)
        return text.lower().strip()
    
    except sr.WaitTimeoutError:
        return "[Error] No speech detected. Please try again."
    except sr.UnknownValueError:
        return "[Error] Could not understand. Please speak clearly."
    except sr.RequestError:
        return "[Error] Speech service unavailable. Check your internet connection."
    except OSError:
        return "[Error] Microphone not found. Please check your microphone."
    except Exception as e:
        return f"[Error] Voice input failed: {e}"


def get_available_voices() -> list:
    """
    List all available TTS voices on this system.
    Useful for finding the right voice_index for config.json.
    
    Returns:
        list: List of dicts with 'index', 'id', and 'name' for each voice
    
    Example:
        voices = get_available_voices()
        for v in voices:
            print(f"Index {v['index']}: {v['name']}")
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    result = []
    for i, voice in enumerate(voices):
        result.append({
            'index': i,
            'id': voice.id,
            'name': voice.name
        })
    engine.stop()
    return result


def reset_engine() -> None:
    """
    Reset the TTS engine. Call this if you change voice settings
    at runtime so they take effect.
    """
    global _engine
    with _engine_lock:
        if _engine:
            try:
                _engine.stop()
            except:
                pass
            _engine = None
