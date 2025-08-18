from .config import settings

try:
    import google.generativeai as genai  # type: ignore
except ImportError:  # pragma: no cover
    genai = None  # Fallback if library not installed

# Try available models in order of preference
AVAILABLE_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.0-pro",
    "gemini-pro"
]
MODEL_NAME = AVAILABLE_MODELS[0]  # Default to first model

def list_available_models():
    """List all available Gemini models for debugging purposes."""
    try:
        available_models = genai.list_models()
        return available_models
    except Exception:
        return None

_LLM_READY = False
if settings.google_api_key and genai is not None:
    try:
        genai.configure(api_key=settings.google_api_key)
        _LLM_READY = True
    except Exception:  # pragma: no cover
        _LLM_READY = False


def generate_answer(prompt: str, temperature: float = 0.2) -> str:
    if not _LLM_READY:
        return "LLM not configured: please set a valid GOOGLE_API_KEY on the server."
    
    # Try multiple models in order until one works
    for model_name in AVAILABLE_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            
            # Add safety settings to avoid prompt rejection
            safety_settings = {
                "HARASSMENT": "BLOCK_NONE",
                "HATE": "BLOCK_NONE",
                "SEXUAL": "BLOCK_NONE",
                "DANGEROUS": "BLOCK_NONE",
            }
            
            response = model.generate_content(
                prompt,
                generation_config={"temperature": temperature},
                safety_settings=safety_settings
            )
            
            return response.text
            
        except Exception:
            continue  # Try the next model
    
    # If all models failed
    return "Error: Unable to generate response with any available model. Please check your API key."
