import gradio as gr
import os
from backend.workflow import create_workflow
from config import GROQ_API_KEY 

if not GROQ_API_KEY:
    raise EnvironmentError("❌ GROQ_API_KEY not found. Please set it in .env file.")

# Initialize workflow
try:
    app = create_workflow()
except Exception as e:
    raise RuntimeError(f"❌ Failed to initialize workflow: {e}")
