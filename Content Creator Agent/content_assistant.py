import os
from typing import TypedDict, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv; load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key is not found in environment variable")

class AgentState(TypedDict):
    topic: str
    content_type: str
    result: Dict[str, str]
    error: str

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7
)

def input_topic(state: AgentState) -> AgentState:
    topic = state.get("topic", "").strip()
    if not topic:
        return {**state, "error": "Topic is required."}
    return {**state, "topic": topic, "error": ""}

def analyze_content_type(state: AgentState) -> AgentState:
    if state.get("error"):
        return state
    valid_types = {"blog", "social", "video", "newsletter"}
    ctype = state.get("content_type", "").lower()
    if ctype not in valid_types:
        return {**state, "error": f"Invalid content_type. Choose from: {list(valid_types)}"}
    return state

def create_content_node(prompt_template: str, output_key: str):
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm | StrOutputParser()

    def node(state: AgentState) -> AgentState:
        if state.get("error"):
            return state
        try:
            result = chain.invoke({"topic": state["topic"]})
            current_result = state.get("result", {})
            return {
                **state,
                "result": {**current_result, output_key: result},
                "error": ""
            }
        except Exception as e:
            return {**state, "error": f"Failed to generate {output_key}: {str(e)}"}
    return node

# Content nodes
write_blog_post = create_content_node(
    "Write a detailed blog post about: {topic}", "blog"
)

create_social_media = create_content_node(
    "Create 3 social media posts (Twitter, LinkedIn, Instagram) about: {topic}", "social"
)

generate_video_script = create_content_node(
    "Generate a video script (with scenes and narration) about: {topic}", "video"
)

create_newsletter = create_content_node(
    "Write a newsletter about: {topic} with subject line and CTA", "newsletter"
)
