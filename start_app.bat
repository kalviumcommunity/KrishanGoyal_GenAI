@echo on
REM Start backend and frontend together

REM Use different ports (8080 and 8502) since the defaults are in use
echo Starting GenAI backend server...
start powershell -NoExit -ExecutionPolicy Bypass -Command "& {cd '%~dp0'; python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8080}"

echo Waiting for backend to initialize...
timeout /t 10 /nobreak > NUL

echo Starting Streamlit frontend...
start powershell -NoExit -ExecutionPolicy Bypass -Command "& {cd '%~dp0'; $env:BACKEND_API_URL='http://localhost:8080'; python -m streamlit run frontend/app.py --server.port 8502}"

echo.
echo Access the UI at: http://localhost:8502
echo.
