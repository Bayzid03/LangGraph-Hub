import logging
import json
from typing import Dict
from .llm import get_llm

logger = logging.getLogger(__name__)

class ActionExtractor:
  def __init__(self):
    try:
      self.model= get_llm(max_new_tokens=512)
      logger.info("Action Extractor initialized with llm")
    except Exception as e:
      logger.error(f"Failed to initialize ActionExtractor: {e}")
      raise

  def extract(self, transcript: str) -> Dict[str, any]:
        if not transcript.strip():
            logger.warning("Empty transcript provided. Returning empty structured output.")
            return {
                "decisions": [],
                "action_items": [],
                "key_points": []
            }

        prompt = """
        Extract from the meeting:
        - decisions made
        - action items (task, owner, deadline)
        - key informational points

        Respond ONLY in JSON format:
        {
          "decisions": ["..."],
          "action_items": [{"task": "...", "owner": "...", "deadline": "..."}],
          "key_points": ["..."]
        }

        Transcript: {transcript}
        """.strip().format(transcript=transcript[:3000])

        try:
            response = self.model.invoke(prompt)
            text = response.content.strip()

            # Clean up code block wrappers
            if text.startswith("```json"):
                text = text[7:-3]
            elif text.startswith("```"):
                text = text[3:-3]

            result = json.loads(text)
            logger.info("Action extraction successful.")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM response: {e}")
            return {
                "error": "parsing_failed",
                "decisions": [],
                "action_items": [],
                "key_points": []
            }
        except Exception as e:
            logger.error(f"Action extraction failed: {str(e)}")
            return {
                "error": "llm_call_failed",
                "decisions": [],
                "action_items": [],
                "key_points": []
            }
