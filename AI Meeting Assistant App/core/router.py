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

# Build graph
def create_router():
    workflow = StateGraph(MeetingState)

    # Node: Classify meeting
    def classify_node(state: MeetingState):
        if not state["transcript"]:
            return {**state, "error": "No transcript provided"}
        try:
            meeting_type = analyzer.classify_meeting(state["transcript"])
            return {**state, "meeting_type": meeting_type, "error": ""}
        except Exception as e:
            return {**state, "error": f"Classification failed: {str(e)}"}

    # Node: Extract structured content
    def extract_node(state: MeetingState):
        if state["error"]:
            return state
        try:
            result = extractor.extract(state["transcript"])
            return {
                **state,
                "decisions": result.get("decisions", []),
                "action_items": result.get("action_items", []),
                "key_points": result.get("key_points", []),
                "error": "extraction_error" if "error" in result else ""
            }
        except Exception as e:
            return {**state, "error": f"Extraction failed: {str(e)}"}

    # Add nodes
    workflow.add_node("classify", classify_node)
    workflow.add_node("extract", extract_node)

    # Set entry point
    workflow.set_entry_point("classify")

    def route_after_classification(state: MeetingState):
        return "extract" if not state["error"] else "__end__"

    workflow.add_conditional_edges(
        "classify",
        route_after_classification,
    )

    workflow.add_edge("extract", "__end__")

    # Return compiled graph
    return workflow.compile()
