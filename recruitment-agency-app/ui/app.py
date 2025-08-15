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

JOB_ROLES = ["Backend Engineer", "Data Scientist", "Product Manager"]

def process_application(resume_file, email, job_role):
    if not resume_file:
        return "⚠️ Please upload a resume (PDF)."
    if not email or "@" not in email:
        return "⚠️ Please enter a valid email address."
    if not job_role:
        return "⚠️ Please select a job role."

    # ✅ resume_file is a string path to the uploaded file
    temp_path = "temp_resume.pdf"

    try:
        # ✅ Copy the file to a known location
        with open(resume_file, "rb") as f_in:
            with open(temp_path, "wb") as f_out:
                f_out.write(f_in.read())  # Copy content
    except Exception as e:
        return f"❌ Failed to process resume: {str(e)}"

    try:
        print(f"Processing application for {email} - {job_role}...")
        final_state = app.invoke({
            "file_path": temp_path,
            "email": email.strip(),
            "job_role": job_role,
            "response": ""
        })
        response = final_state.get("response", "No response from system.")
    except Exception as e:
        response = f"❌ AI Processing Error: {str(e)}. Check API key and internet connection."
        print(f"Error during workflow.invoke: {e}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                print(f"Warning: Could not delete temp file: {e}")

    return response

# ------------------ Gradio UI ------------------
with gr.Blocks(title="📄 Recruitment Agency AI", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Recruitment Agency AI")
    gr.Markdown("""
    **AI-Powered Resume Screening**  
    Upload your PDF resume, enter your email, and select a job role.  
    The AI will assess your fit and send feedback automatically.
    """)

    with gr.Row():
        with gr.Column(scale=2):
            resume_upload = gr.File(
                label="📄 Upload Resume (PDF)",
                file_types=[".pdf"],
                interactive=True
            )
            applicant_email = gr.Textbox(
                label="✉️ Your Email Address",
                placeholder="you@example.com",
                interactive=True
            )
            job_dropdown = gr.Dropdown(
                choices=JOB_ROLES,
                label="🎯 Select Job Role",
                interactive=True
            )
            submit_btn = gr.Button("🚀 Screen My Application", variant="primary")

        with gr.Column(scale=3):
            output = gr.Textbox(
                label="🤖 AI Decision",
                placeholder="Results will appear here...",
                lines=10,
                max_lines=15
            )

    submit_btn.click(
        fn=process_application,
        inputs=[resume_upload, applicant_email, job_dropdown],
        outputs=output
    )

    gr.Markdown("""
    ---
    💡 **Powered by** [LangGraph](https://langchain.com/langgraph) + Llama3 | 
    🔐 Your data is processed securely and deleted immediately after use.
    """)

# Launch the app - this line is critical!
if __name__ == "__main__":
    # Use a safe port; fallback if 7860 is busy
    demo.launch(
        server_name="127.0.0.1",  # Only local
        server_port=7860,
        share=False,             # Set to True for public link
        show_error=True
    )

