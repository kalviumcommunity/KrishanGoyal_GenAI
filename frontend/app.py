import streamlit as st
import requests
import time
import os

# Allow configuration of API URL through environment variable
API_BASE = os.environ.get("BACKEND_API_URL", "http://localhost:8080")

# Must be the first Streamlit command
st.set_page_config(page_title="NCERT Class 12 Assistant", layout="wide")

# Now we can display connection info
st.caption(f"Backend API: {API_BASE}")

st.title("📘 NCERT Class 12 Q&A Assistant")
st.caption("Read-only mode: embeddings pre-built by developer.")

with st.sidebar:
    st.header("Query Settings")
    query_subject = st.selectbox(
        "Subject filter",
        ["Any", "Physics", "Biology", "Math"],
        help="Restrict retrieval to a subject or search all."
    )
    temperature = st.slider(
        "Temperature", 0.0, 1.0, 0.2, 0.05,
        help="Lower = more factual, higher = more creative phrasing."
    )
    
    st.header("Prompt Engineering")
    use_one_shot = st.toggle(
        "Use One-Shot Prompting", 
        value=False,
        help="Enable to use subject-specific example Q&A pairs to guide the model's responses."
    )
    if use_one_shot:
        st.info("One-shot prompting includes an example Q&A pair to guide the model's response format and style.")
        example_subject = "Math"
        if query_subject != "Any":
            example_subject = query_subject
        st.caption(f"Using {example_subject} example")

st.header("Ask a Question")
question = st.text_input("Enter your question", placeholder="Explain the principle of superposition of waves.")

# Helper for API calls with retry logic
def call_api_with_retry(endpoint, json_data, max_retries=3, delay=2):
    """Call API endpoint with retry logic."""
    for attempt in range(max_retries):
        try:
            # Add explicit headers to ensure proper content type
            headers = {'Content-Type': 'application/json'}
            
            # Make sure JSON data is not None for key values
            clean_data = {k: v for k, v in json_data.items() if v is not None}
            
            response = requests.post(
                f"{API_BASE}/{endpoint}", 
                json=clean_data,  # Use json parameter, not data
                headers=headers,
                timeout=10
            )
            
            if not response.ok:
                st.error(f"Error: {response.status_code} - {response.text}")
            return response
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                if attempt == 0:  # Only show this on first failure
                    st.warning(f"Cannot connect to backend API. Retrying {max_retries-1} more times...")
                time.sleep(delay)
            else:
                raise  # Re-raise the exception if all retries failed

ask = st.button("Ask", type="primary")
if ask:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            # Make sure the question is not empty after stripping
            cleaned_question = question.strip() if question else ""
            
            # Only proceed if there's an actual question
            if not cleaned_question:
                st.warning("Please enter a question.")
                st.stop()  # Stop execution instead of return
                
            payload = {
                "question": cleaned_question, 
                "temperature": temperature,
                "use_one_shot": use_one_shot
            }
            if query_subject != "Any":
                payload["subject"] = query_subject
            
            try:
                r = call_api_with_retry("ask", payload)
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend server. Please make sure the backend is running.")
                st.stop()
        if r.ok:
            data = r.json()
            # Check for error messages from backend
            if "error" in data:
                st.error(f"Error: {data['error']}")
            else:
                st.subheader("Answer")
                st.write(data.get("answer", ""))
                
                # Display metadata about the response
                meta_info = f"k={data.get('used_k')} | temp={data.get('temperature')}"
                if data.get("used_one_shot"):
                    meta_info += " | one-shot=True"
                st.caption(meta_info)
                sources = data.get("sources", [])
                if sources:
                    st.caption("Sources:")
                    for s in sources:
                        page = s.get("page")
                        subj = s.get("subject")
                        src = s.get("source")
                        st.markdown(f"- **{subj}** | {src} (page {page})")
        else:
            st.error("Error from server")
