import logging
from .llm import get_llm

logger = logging.getLogger(__name__)

# Supported categories
CATEGORIES = ["Decision", "Project", "Info", "Conflict"]

class MeetingAnalyzer:
    def __init__(self):
        self.model = get_llm(max_new_tokens=10)

    def classify_meeting(self, transcript: str) -> str:
        if not transcript.strip():
            logger.warning("Empty transcript provided. Defaulting to 'Info'.")
            return "Info"

        prompt = f"""
        Classify meeting type: Decision, Project, Info, or Conflict.
        Respond with only one word.

        Transcript: {transcript[:2000]}
        """

        try:
            response = self.model.invoke(prompt)
            raw = response.content.strip()

            for cat in CATEGORIES:
                if cat.lower() in raw.lower():
                    logger.info(f"Classified as: {cat}")
                    return cat

            logger.warning(f"Unrecognized classification output: '{raw}'. Falling back to 'Info'.")
            return "Info"

        except Exception as e:
            logger.error(f"LLM call failed in classify_meeting: {str(e)}")
            return "Info"
