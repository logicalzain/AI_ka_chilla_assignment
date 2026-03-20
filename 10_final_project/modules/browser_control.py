# ============================================================
# browser_control.py — Browser & Web Automation Module
# ============================================================
# This module controls Google Chrome to open websites, search
# YouTube, open WhatsApp Web, and perform Google searches.
#
# HOW IT WORKS:
#   - Uses Python's 'webbrowser' module to open URLs in Chrome
#   - Chrome path is taken from config.json
#   - All commands simply open URLs — no scraping or automation
#
# HOW TO CUSTOMIZE:
#   - Change browser path in config.json "browser_path"
#   - Add new website shortcuts in the WEBSITES dictionary below
# ============================================================

import webbrowser
import urllib.parse

# ============================================================
# WEBSITES: Quick-access website shortcuts
# ------------------------------------------------------------
# HOW TO ADD A NEW WEBSITE:
#   Add an entry like:  "name": "https://url.com"
#   Then you can say: "open name"
# ============================================================
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chat.openai.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://twitter.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "stackoverflow": "https://stackoverflow.com",
    "wikipedia": "https://www.wikipedia.org",
    "amazon": "https://www.amazon.com",
    "netflix": "https://www.netflix.com",
    "spotify": "https://open.spotify.com",
    "google drive": "https://drive.google.com",
    "google maps": "https://maps.google.com",
    "canva": "https://www.canva.com",
    "figma": "https://www.figma.com",
}


def _get_browser(config: dict):
    """
    Get a browser controller for Chrome using the path from config.
    
    Args:
        config (dict): Configuration dictionary from config.json
    
    Returns:
        webbrowser controller or None if Chrome not found
    """
    chrome_path = config.get('browser_path', '')
    if chrome_path:
        try:
            # Register Chrome with the path from config
            webbrowser.register('chrome', None,
                                webbrowser.BackgroundBrowser(chrome_path))
            return webbrowser.get('chrome')
        except Exception:
            pass
    # Fallback to default browser
    return webbrowser


def open_chrome(config: dict) -> str:
    """
    Open Google Chrome browser.
    
    Args:
        config (dict): Configuration dictionary
    
    Returns:
        str: Status message
    """
    try:
        browser = _get_browser(config)
        browser.open("https://www.google.com")
        return "🌐 Chrome opened successfully!"
    except Exception as e:
        return f"❌ Could not open Chrome: {e}"


def open_website(site_name: str, config: dict) -> str:
    """
    Open a website by its shortcut name or full URL.
    
    Args:
        site_name (str): Website name (e.g., "youtube") or full URL
        config (dict): Configuration dictionary
    
    Returns:
        str: Status message
    """
    site_name_lower = site_name.lower().strip()
    
    # --- Check if it's a known shortcut ---
    if site_name_lower in WEBSITES:
        url = WEBSITES[site_name_lower]
    elif site_name.startswith("http"):
        url = site_name
    else:
        # Try to construct a URL
        url = f"https://www.{site_name_lower}.com"
    
    try:
        browser = _get_browser(config)
        browser.open(url)
        return f"🌐 Opening {site_name}..."
    except Exception as e:
        return f"❌ Could not open {site_name}: {e}"


def search_youtube(query: str, config: dict) -> str:
    """
    Search for something on YouTube.
    
    Args:
        query (str): Search query (e.g., "python tutorial")
        config (dict): Configuration dictionary
    
    Returns:
        str: Status message
    """
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        browser = _get_browser(config)
        browser.open(url)
        return f"📺 Searching YouTube for: {query}"
    except Exception as e:
        return f"❌ YouTube search failed: {e}"


def search_google(query: str, config: dict) -> str:
    """
    Search Google for something.
    
    Args:
        query (str): Search query
        config (dict): Configuration dictionary
    
    Returns:
        str: Status message
    """
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded_query}"
        browser = _get_browser(config)
        browser.open(url)
        return f"🔍 Searching Google for: {query}"
    except Exception as e:
        return f"❌ Google search failed: {e}"


def open_whatsapp(config: dict) -> str:
    """
    Open WhatsApp Web in Chrome.

    Args:
        config (dict): Configuration dictionary

    Returns:
        str: Status message
    """
    try:
        browser = _get_browser(config)
        browser.open("https://web.whatsapp.com")
        return "💬 Opening WhatsApp Web..."
    except Exception as e:
        return f"❌ Could not open WhatsApp: {e}"


def send_whatsapp_message(phone: str, message: str, config: dict) -> str:
    """
    Open WhatsApp Web with a pre-filled message to a specific phone number.

    Uses the wa.me deep-link so WhatsApp Web opens with the contact
    and message ready to send. The user just clicks Send.

    Args:
        phone (str): Phone number with country code (e.g. "923001234567")
        message (str): Message text to pre-fill
        config (dict): Configuration dictionary

    Returns:
        str: Status message
    """
    # Clean phone number: keep only digits and leading +
    clean_phone = ''.join(c for c in phone if c.isdigit() or c == '+')
    clean_phone = clean_phone.lstrip('+')  # wa.me wants just digits

    if not clean_phone or len(clean_phone) < 6:
        return ("❌ Invalid phone number. Use format:\n"
                "  send whatsapp <country_code><number> <message>\n"
                "  Example: send whatsapp 923001234567 Hello how are you?")

    try:
        encoded_msg = urllib.parse.quote(message)
        url = f"https://wa.me/{clean_phone}?text={encoded_msg}"
        browser = _get_browser(config)
        browser.open(url)
        return (f"💬 Opening WhatsApp for +{clean_phone}...\n"
                f"Message: \"{message}\"\n"
                f"Just click Send in WhatsApp Web!")
    except Exception as e:
        return f"❌ Could not open WhatsApp: {e}"


def play_youtube_video(query: str, config: dict) -> str:
    """
    Search and open the first YouTube result for a query.
    (Opens search results — user picks the video)

    Args:
        query (str): What to play
        config (dict): Configuration dictionary

    Returns:
        str: Status message
    """
    return search_youtube(query, config)


def get_available_websites() -> str:
    """
    List all available website shortcuts.

    Returns:
        str: Formatted list of available websites
    """
    result = "🌐 Available website shortcuts:\n"
    for name, url in sorted(WEBSITES.items()):
        result += f"  → {name}: {url}\n"
    return result.strip()

