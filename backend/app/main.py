from fastapi import FastAPI, UploadFile, File, Form, Body, Request
from typing import List, Optional
import json
from pathlib import Path
from .config import settings
from .rag_pipeline import answer_question

# Only import ingestion-related modules if not read-only to avoid unnecessary deps at runtime
if not settings.read_only:
    from . import pdf_processing  # type: ignore
    from .embedding_store import add_texts, reset_index  # type: ignore

app = FastAPI(title="NCERT Class 12 RAG Assistant")

PDF_DIR = Path("data/raw_pdfs")

# Register ingestion + reset endpoints only when not in read-only mode
if not settings.read_only:
    @app.post("/ingest")
    async def ingest_pdfs(subject: str = Form(...), files: List[UploadFile] = File(...)):
        all_chunks = []
        metadata = []
        for f in files:
            pdf_path = PDF_DIR / f.filename
            content = await f.read()
            pdf_path.write_bytes(content)
            chunks, meta = pdf_processing.extract_chunks_with_metadata(pdf_path, subject, settings.chunk_size, settings.chunk_overlap)
            all_chunks.extend(chunks)
            metadata.extend(meta)
        add_texts(all_chunks, metadata)
        return {"ingested_files": [f.filename for f in files], "chunks": len(all_chunks)}

@app.post("/ask")
async def ask(
    request: Request,
    question: Optional[str] = Form(None),
    temperature: Optional[float] = Form(None),
    subject: Optional[str] = Form(None),
    use_one_shot: Optional[bool] = Form(False),
    use_multi_shot: Optional[bool] = Form(False),
    json_body: Optional[dict] = Body(None)
):
    # Support both form-data (Streamlit current) and JSON clients
    
    # Handle direct JSON body (not through Body parameter)
    body_bytes = await request.body()
    if body_bytes:
        try:
            if request.headers.get("content-type") == "application/json":
                body_data = json.loads(body_bytes.decode())
                if question is None:  # Only override if not provided via Form
                    question = body_data.get("question")
                if temperature is None:  # Only override if not provided via Form
                    temperature = body_data.get("temperature")
                if subject is None:  # Only override if not provided via Form
                    subject = body_data.get("subject")
                if use_one_shot is False:  # Only override if not provided via Form
                    use_one_shot = body_data.get("use_one_shot", False)
                if use_multi_shot is False:  # Only override if not provided via Form
                    use_multi_shot = body_data.get("use_multi_shot", False)
                k = body_data.get("k")
        except Exception:
            pass  # Silently continue if JSON parsing fails
    
    # Handle Body parameter if it's used
    if json_body:
        # Extract values from JSON body
        if question is None:  # Only override if not provided via Form
            question = json_body.get("question")
        if temperature is None:  # Only override if not provided via Form  
            temperature = json_body.get("temperature")
        if subject is None:  # Only override if not provided via Form
            subject = json_body.get("subject")
        if use_one_shot is False:  # Only override if not provided via Form
            use_one_shot = json_body.get("use_one_shot", False)
        if use_multi_shot is False:  # Only override if not provided via Form
            use_multi_shot = json_body.get("use_multi_shot", False)
        k = json_body.get("k")
    else:
        k = None
    
    # Validate that question is not None or empty
    if not question:
        return {"error": "Question cannot be empty"}
        
    try:
        result = answer_question(
            question, 
            temperature=temperature, 
            subject=subject, 
            k=k,
            use_one_shot=use_one_shot,
            use_multi_shot=use_multi_shot
        )
        return result
    except Exception as e:
        return {
            "error": "An error occurred while processing your question",
            "details": str(e)
        }

@app.get("/health")
async def health():
    return {"status": "ok"}


if not settings.read_only:
    @app.post("/reset_index")
    async def reset():
        reset_index()
        return {"status": "cleared"}
