import yaml
import os
from logger import logger

def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        logger.error(f"Configuration file not found at: {config_path}")
        return None

    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            logger.info("Configuration loaded successfully.")
            return config
    except Exception as e:
        logger.error(f"Error parse config YAML: {e}")
        return None
