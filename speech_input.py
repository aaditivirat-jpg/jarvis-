import speech_recognition as sr
from logger import logger
from voice_output import speak

class SpeechInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        # Dynamically adjust for ambient noise
        self.recognizer.dynamic_energy_threshold = True
        
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                logger.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Microphone calibrated.")
        except Exception as e:
            logger.error(f"Microphone init failed! Is your mic plugged in? Are Windows Privacy settings blocking it? Error: {e}")
            self.microphone = None

    def wait_for_wake_word(self, wake_word):
        """Continuously listens until the wake word is detected."""
        if not self.microphone: return False
        
        wake_word = wake_word.lower()
        logger.info(f"Waiting for wake word: '{wake_word}'...")

        with self.microphone as source:
            while True:
                try:
                    # short timeout/phrase_time_limit to keep it snappy
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=3)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    if wake_word in text:
                        logger.info(f"Wake word detected! (Heard: '{text}')")
                        speak("Yes sir?")
                        return True
                        
                except sr.WaitTimeoutError:
                    continue # Keep listening
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    pass
                except sr.RequestError as e:
                    logger.error(f"Could not request results from Speech Recognition service; {e}")
                    # Usually means network issue
                    import time
                    time.sleep(2)

    def listen_for_command(self):
        """Listens for the actual command after wake word is triggered."""
        if not self.microphone: return ""
        
        logger.info("Listening for command...")
        with self.microphone as source:
            try:
                # Give user ~5 seconds to speak their command
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                logger.info("Processing command audio...")
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.WaitTimeoutError:
                logger.warning("Listening for command timed out.")
                return ""
            except sr.UnknownValueError:
                logger.warning("Could not understand command.")
                speak("I didn't catch that.")
                return ""
            except sr.RequestError as e:
                logger.error(f"Speech Recognition service error: {e}")
                speak("I'm having trouble connecting to the speech service.")
                return ""
