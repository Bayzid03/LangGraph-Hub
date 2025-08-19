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

