import time
from logger import logger
from config_loader import load_config
from speech_input import SpeechInput
from command_processor import CommandProcessor
from voice_output import speak

def main():
    logger.info("Initializing Jarvis Assistant...")

    # 1. Load config
    config = load_config()
    if not config:
        logger.error("Failed to start without configuration. Exiting.")
        return

    # 2. Setup Modules
    settings = config.get("settings", {})
    wake_word = settings.get("wake_word", "hey jarvis")
    
    speech_handler = SpeechInput()
    if not speech_handler.microphone:
        logger.error("Microphone missing. Cannot start voice loops.")
        return

    processor = CommandProcessor(config)
    speak("System is online and ready.")

    # 3. Main Loop
    while True:
        try:
            # Block until wake word is heard
            wakened = speech_handler.wait_for_wake_word(wake_word)
            
            if wakened:
                # Capture the command
                command_text = speech_handler.listen_for_command()
                
                if command_text:
                    logger.info(f"User said: {command_text}")
                    # Process and execute
                    processor.process(command_text)
                    
            # Brief pause before cycling to prevent spamming
            time.sleep(0.5)

        except KeyboardInterrupt:
            logger.info("Shutting down via KeyboardInterrupt...")
            speak("Shutting down.")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
