# Development Guide

## Setup

1. Create virtual env (recommended)
2. pip install -r requirements.txt
3. Copy .env.example to .env and fill GOOGLE_API_KEY

## Run

PowerShell:

```
powershell -ExecutionPolicy Bypass -File backend/run_api.ps1
powershell -ExecutionPolicy Bypass -File frontend/run_ui.ps1
```

Backend: http://localhost:8000/docs
Frontend: http://localhost:8501

## Ingestion Flow (One-Time, Developer Only)

Developer performs embedding once, producing persistent artifacts in `vector_store` (FAISS index + JSONL metadata/text). End-users operate only in read-only query mode.

### Steps

1. Place NCERT PDFs into `data/raw_pdfs/`.
2. Run offline ingestion (preferred):
   ```
   python -m backend.app.offline_ingest               # auto subject inference
   python -m backend.app.offline_ingest --pattern leph*.pdf --subject Physics
   ```
   or temporarily set `READ_ONLY_MODE=false` and use the sidebar ingestion UI.
3. Verify files created: `vector_store/index.faiss`, `metadata.jsonl`, `texts.jsonl`, `state.json`.
4. Set `READ_ONLY_MODE=true` in `.env` before deploying so users cannot modify embeddings.

To rebuild from scratch: delete `vector_store` or call a (future) admin reset endpoint, then re-run ingestion.

## Ask Flow

Question -> similarity search -> Gemini generation with constrained prompt.

## TODO / Next Steps

- Better chunking by headings
- Source citation with page numbers
- Add hybrid retrieval (BM25 + FAISS)
- Chat history & follow-ups
- Evaluation scripts (retrieval accuracy)
