# ============================================================
# main.py — JEEVES Desktop Assistant Entry Point
# ============================================================
# This is the MAIN FILE you run to start the assistant.
#
# HOW TO RUN:
#   python main.py
#
# WHAT IT DOES:
#   1. Loads configuration from config.json
#   2. Initializes all modules
#   3. Launches the GUI window
#   4. Handles graceful shutdown on exit
#
# FIRST TIME SETUP:
#   1. Install dependencies: pip install -r requirements.txt
#   2. Edit config.json with your settings (optional)
#   3. Run: python main.py
# ============================================================

import json
import os
import sys

def load_config() -> dict:
    """
    Load configuration from config.json.
    
    If config.json doesn't exist, creates a default one.
    
    Returns:
        dict: Configuration dictionary
    """
    # --- Find the config file path (same directory as this script) ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')
    
    # --- Default configuration ---
    default_config = {
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
        "search_directories": ["C:/Users", "D:/", "E:/"],
        "screenshot_save_path": "",
        "greeting_enabled": True
    }
    
    # --- Try to load existing config ---
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            # Merge with defaults (add any missing keys)
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config
        except json.JSONDecodeError:
            print("[Warning] config.json is corrupted. Using defaults.")
            return default_config
    else:
        # --- Create default config file ---
        try:
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"[Info] Created default config at: {config_path}")
        except Exception as e:
            print(f"[Warning] Could not create config file: {e}")
        return default_config


def main():
    """
    Main entry point for the JEEVES Desktop Assistant.
    
    Loads config, starts the GUI, and handles errors.
    """
    print("=" * 50)
    print("  🤖 JEEVES Desktop Assistant")
    print("  Starting up...")
    print("=" * 50)
    
    # --- Load configuration ---
    config = load_config()
    print(f"  Assistant: {config.get('assistant_name', 'Jeeves')}")
    print(f"  User: {config.get('user_name', 'Boss')}")
    print(f"  AI: {'Configured' if config.get('gemini_api_key') else 'Not configured'}")
    print("=" * 50)
    
    # --- Make sure we can import our modules ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    try:
        # --- Import and launch GUI ---
        from gui.app_gui import JeevesGUI
        
        app = JeevesGUI(config)
        app.run()
        
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")
        print("   Then try again.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error starting JEEVES: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
