from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from config import GROQ_API_KEY
import os

class State(TypedDict):
    file_path: str
    email: str
    job_role: str
    application: str
    job_description: str
    experience_level: str
    skill_match: bool
    response: str
