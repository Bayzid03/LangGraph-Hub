import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Email
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Paths
JOB_DESCRIPTIONS_DIR = "data/job_descriptions"