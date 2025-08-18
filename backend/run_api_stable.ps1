# Run FastAPI without hot reload (more stable)
uvicorn backend.app.main:app --host 0.0.0.0 --port 8080 --no-server-header
