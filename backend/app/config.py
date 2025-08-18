import os
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

# Get the project root directory (2 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Load .env from project root
dotenv_path = PROJECT_ROOT / '.env'
load_dotenv(dotenv_path=dotenv_path)

class Settings(BaseModel):
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    persist_directory: str = os.getenv("PERSIST_DIRECTORY", os.getenv("VECTOR_STORE_DIR", "vector_store"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", 800))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", 120))
    read_only: bool = os.getenv("READ_ONLY_MODE", "false").lower() in {"1", "true", "yes"}
    max_retrieve: int = int(os.getenv("MAX_RETRIEVE", 6))
    temperature_default: float = float(os.getenv("TEMPERATURE_DEFAULT", 0.2))

settings = Settings()
