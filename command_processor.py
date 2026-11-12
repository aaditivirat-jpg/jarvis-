from thefuzz import process
from logger import logger
from action_executor import execute_command_actions
from voice_output import speak
from llm_agent import LLMAgent

class CommandProcessor:
    def __init__(self, config):
        self.config = config
        self.settings = config.get("settings", {})
        self.commands_list = config.get("commands", [])
        
        # Initialize conversatonal fallback
        api_key = self.settings.get("gemini_api_key")
        self.llm_agent = LLMAgent(api_key)

        self.fuzzy_threshold = self.settings.get("fuzzy_threshold", 75)
        self.alias_to_command = self._build_alias_map()

    def _build_alias_map(self):
        """Creates a flat dictionary mapping all aliases to their full command config."""
        mapping = {}
        for cmd in self.commands_list:
            aliases = cmd.get("aliases", [])
            for alias in aliases:
                mapping[alias.lower()] = cmd
            # Map the primary name as well just in case
            mapping[cmd.get("name").lower()] = cmd
        return mapping

    def process(self, spoken_text):
        """
        Takes raw spoken text, matches it against commands, and executes.
        """
        spoken_text = spoken_text.lower().strip()
        if not spoken_text:
            return

        logger.info(f"Processing text: '{spoken_text}'")

        # Get list of all known aliases to match against
        choices = list(self.alias_to_command.keys())
        
        # thefuzz process.extractOne returns the best match: (matched_string, score)
        best_match = process.extractOne(spoken_text, choices)

        if best_match:
            matched_phrase, score = best_match
            logger.info(f"Fuzzy Matched: '{matched_phrase}' with score {score}")

            if score >= self.fuzzy_threshold:
                target_command = self.alias_to_command[matched_phrase]
                logger.info(f"Executing command: {target_command.get('name')}")
                execute_command_actions(target_command)
            else:
                logger.warning(f"Below fuzzy threshold. Routing string to LLM: '{spoken_text}'")
                llm_response = self.llm_agent.query(spoken_text)
                speak(llm_response)
        else:
            logger.warning("No matches found. Routing string to LLM.")
            llm_response = self.llm_agent.query(spoken_text)
            speak(llm_response)
