import os
import subprocess
from logger import logger
from voice_output import speak

def execute_command_actions(command_config):
    """
    Executes the actions associated with a recognized command.
    command_config is the dict from config.yaml under 'commands'
    """
    # 1. Provide voice response
    response_text = command_config.get("response")
    if response_text:
        speak(response_text)

    # 2. Open applications
    applications = command_config.get("applications", [])
    if not applications:
        logger.warning(f"No applications configured to launch for command: {command_config.get('name')}")
        return

    for app_path in applications:
        launch_application(app_path)

def launch_application(path):
    """
    Safely open a path Windows style.
    Handles standard executables and registered file types / URLs.
    """
    logger.info(f"Attempting to launch: {path}")
    
    if not os.path.exists(path) and not path.startswith("http"):
        # We might have cases like 'calc.exe' which are in PATH but os.path.exists fails without full path
        # Let's try it anyway using Popen or os.startfile but warn first
        logger.warning(f"Path does not exist directly: {path}. Trying system launch.")

    try:
        # os.startfile acts exactly like double-clicking the file in Windows Explorer
        os.startfile(path)
        logger.info(f"Successfully started: {path}")
    except FileNotFoundError:
        logger.error(f"Failed to start file (Not Found): {path}")
    except Exception as e:
        # Fallback to subprocess if startfile fails for weird reasons
        try:
            logger.info("os.startfile failed. Trying subprocess.Popen...")
            subprocess.Popen([path], shell=True)
            logger.info(f"Successfully started via subprocess: {path}")
        except Exception as ex:
            logger.error(f"Failed to launch application '{path}': {ex}")
            speak("I encountered an error trying to launch an application.")
