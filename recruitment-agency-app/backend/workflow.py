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

def extract_resume(state: State) -> State:
    from backend.resume_processor import extract_text_from_pdf
    text = extract_text_from_pdf(state["file_path"])
    return {**state, "application": text}

def load_job_description(state: State) -> State:
    path = os.path.join("data/job_descriptions", f"{state['job_role'].lower().replace(' ', '_')}.txt")
    with open(path, "r") as f:
        jd = f.read()
    return {**state, "job_description": jd}

def categorize_experience(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Based on this application, classify experience as: entry-level, mid-level, senior-level.\n\nApplication: {application}"
    )
    chain = prompt | llm
    level = chain.invoke({"application": state["application"]}).content.strip().lower()
    return {**state, "experience_level": level}

def assess_skillset(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        """
        Compare the candidate's application to the job description.
        Respond only with 'True' if matched, otherwise 'False'.

        Job: {job_description}
        Candidate: {application}
        """
    )
    chain = prompt | llm
    match_str = chain.invoke({
        "job_description": state["job_description"],
        "application": state["application"]
    }).content.strip()
    match = "true" in match_str.lower()
    return {**state, "skill_match": match}

def schedule_interview(state: State) -> State:
    return {**state, "response": "✅ Shortlisted: HR interview will be scheduled."}

def escalate_to_recruiter(state: State) -> State:
    return {**state, "response": "⚠️ Senior candidate, but skills don't match. Escalated for review."}

def reject_and_email(state: State) -> State:
    from backend.email_sender import send_rejection_email
    sent = send_rejection_email(state["email"])
    status = "Sent" if sent else "Failed"
    return {**state, "response": f"❌ Not qualified. Rejection email: {status}"}

# ------------------ Conditional Routing ------------------
def route_decision(state: State):
    if state["skill_match"]:
        return "schedule_interview"
    elif state["experience_level"] == "senior-level":
        return "escalate_to_recruiter"
    else:
        return "reject_and_email"

# ------------------ Build Graph ------------------
def create_workflow():
    workflow = StateGraph(State)

    workflow.add_node("extract_resume", extract_resume)
    workflow.add_node("load_job_description", load_job_description)
    workflow.add_node("categorize_experience", categorize_experience)
    workflow.add_node("assess_skillset", assess_skillset)
    workflow.add_node("schedule_interview", schedule_interview)
    workflow.add_node("escalate_to_recruiter", escalate_to_recruiter)
    workflow.add_node("reject_and_email", reject_and_email)

    workflow.set_entry_point("extract_resume")
    workflow.add_edge("extract_resume", "load_job_description")
    workflow.add_edge("load_job_description", "categorize_experience")
    workflow.add_edge("categorize_experience", "assess_skillset")
    workflow.add_conditional_edges("assess_skillset", route_decision)
    workflow.add_edge("schedule_interview", END)
    workflow.add_edge("escalate_to_recruiter", END)
    workflow.add_edge("reject_and_email", END)

    return workflow.compile()
