from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph
from .analyzer import MeetingAnalyzer
from .action_extractor import ActionExtractor

# Define state
class MeetingState(TypedDict):
    transcript: str
    meeting_type: str
    decisions: list
    action_items: list
    key_points: list
    error: str

# Initialize components
analyzer = MeetingAnalyzer()
extractor = ActionExtractor()
