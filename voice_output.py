import pyttsx3
from logger import logger

class VoiceOutput:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.setup_voice()
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None

    def setup_voice(self):
        """Configure voice properties (rate, volume, etc)"""
        if not self.engine: return
        
        voices = self.engine.getProperty('voices')
        # Try to find a male voice or just select the first one
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 170) # slightly slower, more natural speed
        self.engine.setProperty('volume', 1.0)

    def speak(self, text):
        """Speaks text synchronously."""
        if not self.engine:
            logger.warning(f"TTS offline. Would have said: {text}")
            return

        logger.info(f"Jarvis: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS Error: {e}")

# Global instance for easy use
speaker = VoiceOutput()

def speak(text):
    speaker.speak(text)
