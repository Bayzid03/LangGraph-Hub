import os
import logging
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from functools import lru_cache

# Configure module-level logger
logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_llm(max_new_tokens=10):
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        logger.error("HUGGINGFACE_API_KEY not set.")
        raise ValueError("HUGGINGFACE_API_KEY is required")

    try:
        logger.info(f"Initializing Hugging Face LLM with max_new_tokens={max_new_tokens}")
        
        llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
            task="text-generation",
            max_new_tokens=max_new_tokens,
            temperature=0.3,
            huggingface_api_key=api_key,
            timeout=30,
        )
        model = ChatHuggingFace(llm=llm)
        
        logger.info("LLM initialized successfully.")
        return model

    except Exception as e:
        logger.error(f"Failed to initialize LLM: {str(e)}")
        raise
