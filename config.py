import os
from dotenv import load_dotenv

# Load environment variables from .env file in development
if os.path.exists(".env"):
    load_dotenv()

# Configuration class
class Config:
    # Ollama settings
    OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434/api/generate")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    
    # Data paths
    VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", "vector_store")
    
    # Other settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Create config instance
config = Config()