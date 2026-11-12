import os
from google import genai
from logger import logger
from voice_output import speak

class LLMAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        # Check if API key is valid (not empty and not the default placeholder)
        if not self.api_key or "YOUR_API_KEY_HERE" in self.api_key:
            logger.warning("Gemini API Key is missing or invalid in config.yaml. Conversational capabilities disabled.")
            self.client = None
        else:
            try:
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Initializing Google Gemini client...")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.client = None

        # System instructions to keep responses short and natural since Jarvis speaks them
        self.system_instruction = (
            "You are Jarvis, a highly intelligent voice assistant. "
            "Keep your responses very concise, natural, and conversational because they are being spoken aloud by a TTS engine. "
            "Do not use markdown, emojis, asterisks, or complex formatting. Just plain conversational text."
        )

    def query(self, prompt_text):
        if not self.client:
            return "Sir, my conversational systems are offline because the Gemini API key is missing."
        
        try:
            logger.info("Sending query to Gemini...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_text,
                config={'system_instruction': self.system_instruction}
            )
            return response.text
        except Exception as e:
            logger.error(f"Error communicating with Gemini: {e}")
            return "I'm sorry sir, I encountered an error while processing your request."

