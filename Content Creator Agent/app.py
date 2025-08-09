import gradio as gr
from content_assistant import run_assistant

def generate_content(topic, content_type):
    if not topic.strip():
        return "Topic is required.", None
    response = run_assistant(topic, content_type)
    if response["success"]:
        output = "\n\n".join([f"**{k}**:\n{v}" for k, v in response["output"].items()])
        return "", output
    else:
        return response["error"], None

interface = gr.Interface(
    fn=generate_content,
    inputs=[
        gr.Textbox(label="Topic", placeholder="e.g., Benefits of Solar Energy"),
        gr.Dropdown(["blog", "social", "video", "newsletter"], label="Content Type")
    ],
    outputs=[
        gr.Textbox(label="Error"),
        gr.Markdown(label="Generated Content")
    ],
    title="Content Creator Assistant",
    description="Generate blog, social, video, or newsletter content using Gemini + LangGraph."
)

if __name__ == "__main__":
    interface.launch()
