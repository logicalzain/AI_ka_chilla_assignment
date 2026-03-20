# ============================================================
# ai_module.py — Google Gemini AI Integration Module
# ============================================================
# This module connects to Google's Gemini AI for:
#   - Answering questions
#   - Researching topics
#   - Having conversations
#   - Generating text/code
#
# HOW IT WORKS:
#   - If API key is set in config.json → uses Gemini API
#   - If no API key → suggests browser search as fallback
#
# HOW TO GET YOUR API KEY:
#   1. Go to: https://aistudio.google.com/app/apikey
#   2. Click "Create API Key"
#   3. Copy the key
#   4. Paste it in config.json under "gemini_api_key"
#   OR use the Settings panel in the app to enter it
#
# HOW TO CUSTOMIZE:
#   - Change the model by editing GEMINI_MODEL below
#   - Change the system prompt in SYSTEM_PROMPT below
#   - Adjust max_tokens, temperature in the ask() function
# ============================================================

# ============================================================
# CONFIGURATION: Change these to customize the AI behavior
# ============================================================

# --- Which Gemini model to use ---
# Options: "gemini-2.0-flash" (fast), "gemini-2.0-pro" (smart)
GEMINI_MODEL = "gemini-2.0-flash"

# --- System prompt: Tells the AI how to behave ---
SYSTEM_PROMPT = """You are Jeeves, a helpful and friendly desktop assistant. 
You help the user with questions, research, coding, and general tasks.
Keep your answers clear, concise, and helpful. 
If you don't know something, say so honestly.
Use emojis occasionally to be friendly. 🤖"""


class AIModule:
    """
    Google Gemini AI integration for the desktop assistant.
    
    Handles API initialization, conversation history, and question answering.
    
    Usage:
        ai = AIModule(config)
        if ai.is_available:
            response = ai.ask("What is Python?")
    """
    
    def __init__(self, config: dict):
        """
        Initialize the AI module with the API key from config.
        
        Args:
            config (dict): Configuration dictionary from config.json
        """
        self.config = config
        self.api_key = config.get('gemini_api_key', '')
        self.is_available = False  # Will be set to True if API connects
        self.model = None
        self.chat = None
        self.conversation_history = []  # Track conversation for context
        
        # --- Try to initialize if API key is provided ---
        if self.api_key:
            self._initialize()
    
    def _initialize(self) -> bool:
        """
        Initialize the Gemini API with the stored API key.
        
        Returns:
            bool: True if initialization successful
        """
        try:
            import google.generativeai as genai
            
            # --- Configure the API with our key ---
            genai.configure(api_key=self.api_key)
            
            # --- Create the model ---
            self.model = genai.GenerativeModel(
                model_name=GEMINI_MODEL,
                system_instruction=SYSTEM_PROMPT
            )
            
            # --- Start a chat session (maintains conversation context) ---
            self.chat = self.model.start_chat(history=[])
            
            self.is_available = True
            return True
        except ImportError:
            self.is_available = False
            return False
        except Exception as e:
            self.is_available = False
            print(f"[AI Module] Initialization error: {e}")
            return False
    
    def set_api_key(self, api_key: str) -> str:
        """
        Set or update the API key at runtime.
        
        Args:
            api_key (str): The Google AI Studio API key
        
        Returns:
            str: Status message
        """
        self.api_key = api_key.strip()
        self.config['gemini_api_key'] = self.api_key
        
        if self._initialize():
            return "✅ API key set! Gemini AI is now ready."
        else:
            return "❌ Invalid API key or connection error. Please check your key."
    
    def ask(self, question: str) -> str:
        """
        Ask the AI a question and get a response.
        
        Uses conversation history for context, so follow-up questions work.
        
        Args:
            question (str): The question or prompt to send to Gemini
        
        Returns:
            str: AI's response, or error/fallback message
        """
        # --- Check if API is available ---
        if not self.is_available:
            if not self.api_key:
                return ("🤖 AI is not configured. To use AI features:\n"
                        "  1. Get an API key from: https://aistudio.google.com/app/apikey\n"
                        "  2. Enter it in Settings → API Key\n"
                        "  OR add it to config.json under 'gemini_api_key'\n\n"
                        "💡 Meanwhile, I can search the web for you! Try: 'search google <query>'")
            else:
                # Try to reinitialize
                if not self._initialize():
                    return "❌ Could not connect to Gemini AI. Check your API key and internet."
        
        try:
            # --- Send message to Gemini ---
            response = self.chat.send_message(question)
            
            # --- Save to conversation history ---
            self.conversation_history.append({
                "user": question,
                "assistant": response.text
            })
            
            return f"🤖 {response.text}"
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "limit" in error_msg.lower():
                return "❌ API quota exceeded. Please wait or check your API plan."
            elif "invalid" in error_msg.lower() or "key" in error_msg.lower():
                return "❌ Invalid API key. Please check your key in Settings."
            else:
                return f"❌ AI error: {error_msg}"
    
    def research(self, topic: str) -> str:
        """
        Research a topic using AI (more detailed than ask).
        
        Args:
            topic (str): Topic to research
        
        Returns:
            str: Detailed research response
        """
        prompt = f"""Please provide a comprehensive but concise research summary on: {topic}
        
Include:
- Key facts and overview
- Important details
- Current relevance
- Useful resources or next steps

Keep it informative and well-organized."""
        
        return self.ask(prompt)
    
    def summarize(self, text: str) -> str:
        """
        Summarize a piece of text using AI.
        
        Args:
            text (str): Text to summarize
        
        Returns:
            str: Summary
        """
        prompt = f"Please summarize the following text concisely:\n\n{text}"
        return self.ask(prompt)
    
    def generate_code(self, description: str) -> str:
        """
        Generate code based on a description.
        
        Args:
            description (str): What code to generate
        
        Returns:
            str: Generated code with explanation
        """
        prompt = f"""Generate code for the following:
{description}

Please provide:
1. The code with comments
2. A brief explanation of how it works
3. How to use it"""
        
        return self.ask(prompt)
    
    def clear_history(self) -> str:
        """
        Clear conversation history and start fresh.
        
        Returns:
            str: Confirmation message
        """
        self.conversation_history = []
        if self.model:
            self.chat = self.model.start_chat(history=[])
        return "🤖 Conversation history cleared. Starting fresh!"
    
    def get_status(self) -> str:
        """
        Get the current status of the AI module.
        
        Returns:
            str: Status information
        """
        if self.is_available:
            return f"🤖 AI Status: ✅ Connected (Model: {GEMINI_MODEL})"
        elif self.api_key:
            return "🤖 AI Status: ❌ API key set but connection failed"
        else:
            return "🤖 AI Status: ❌ No API key configured"
