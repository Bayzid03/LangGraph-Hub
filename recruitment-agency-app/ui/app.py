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
