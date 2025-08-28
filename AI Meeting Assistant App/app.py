import gradio as gr
from core.transcriber import AudioTranscriber
from core.router import create_router

transcriber = AudioTranscriber(model_size="small")
workflow = create_router()

def process_meeting(audio_file):
    # Step 1: Transcribe
    transcript = transcriber.transcribe(audio_file)
    if not transcript:
        return "❌ Transcription failed.", None

    # Step 2: Run workflow
    try:
        result = workflow.invoke({"transcript": transcript, "error": ""})
        if result["error"]:
            return f"❌ Processing error: {result['error']}", None

        # Format output
        md = f"""
        ### ✅ Meeting Type: {result['meeting_type']}

        #### Decisions:
        {'<br>'.join(f"- {d}" for d in result['decisions']) or 'None'}

        #### Action Items:
        {'<br>'.join(f"- {a['task']} (Owner: {a['owner']}, Deadline: {a.get('deadline', 'N/A')})" for a in result['action_items']) or 'None'}

        #### Key Points:
        {'<br>'.join(f"- {p}" for p in result['key_points']) or 'None'}
        """
        return "✅ Success!", md
    except Exception as e:
        return f"❌ Workflow error: {str(e)}", None

# Gradio Interface
interface = gr.Interface(
    fn=process_meeting,
    inputs=gr.Audio(sources=["upload"], type="filepath"),
    outputs=["text", "markdown"],
    title="🎙️ AI Meeting Assistant",
    description="Upload a meeting audio to get decisions, actions, and key points."
)

if __name__ == "__main__":
    interface.launch()
