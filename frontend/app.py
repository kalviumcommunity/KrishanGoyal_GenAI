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
    
    # Create a radio button for prompt type
    prompt_type = st.radio(
        "Prompting Technique",
        ["Zero-Shot", "One-Shot", "Multi-Shot", "Dynamic"],
        index=0,
        help="Select the prompt engineering technique to use"
    )
    
    use_zero_shot = False
    use_one_shot = False
    use_multi_shot = False
    use_dynamic = False
    
    if prompt_type == "Zero-Shot":
        use_zero_shot = True
        st.info("Zero-shot prompting relies solely on the model's knowledge without example Q&A pairs, using only clear instructions.")
    elif prompt_type == "One-Shot":
        use_one_shot = True
        st.info("One-shot prompting includes a single example Q&A pair to guide the model's response format and style.")
    elif prompt_type == "Multi-Shot":
        use_multi_shot = True
        st.info("Multi-shot prompting includes multiple example Q&A pairs to guide the model's response format and style.")
    elif prompt_type == "Dynamic":
        use_dynamic = True
        st.info("Dynamic prompting automatically adapts the response format based on the type of question asked.")
        
        # Show the different question types that can be detected
        with st.expander("Question Types Detected"):
            st.markdown("""
            - **Definition**: What is...?, Define..., Explain the concept of...
            - **Comparison**: Compare..., Difference between..., Contrast...
            - **Process**: Process of..., Steps in..., How does...
            - **Problem-Solving**: Solve..., Calculate..., Find...
            - **Application**: Application of..., Used for..., Importance of...
            """)
    
    if use_one_shot or use_multi_shot:
        example_subject = "Math"
        if query_subject != "Any":
            example_subject = query_subject
        st.caption(f"Using {example_subject} examples")
        
        # Show more details about number of examples for multi-shot
        if use_multi_shot:
            examples_count = {"Physics": 3, "Biology": 3, "Math": 3}
            count = examples_count.get(example_subject, 3)
            st.caption(f"Using {count} example Q&A pairs")

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
                "use_zero_shot": use_zero_shot,
                "use_one_shot": use_one_shot,
                "use_multi_shot": use_multi_shot,
                "use_dynamic": use_dynamic
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
                if data.get("used_zero_shot"):
                    meta_info += " | zero-shot=True"
                if data.get("used_one_shot"):
                    meta_info += " | one-shot=True"
                if data.get("used_multi_shot"):
                    meta_info += " | multi-shot=True"
                if data.get("used_dynamic"):
                    question_type = data.get("question_type", "unknown")
                    meta_info += f" | dynamic=True (type: {question_type})"
                
                # Add token usage if available
                token_counts = data.get("token_counts")
                if token_counts:
                    meta_info += f" | tokens: {token_counts.get('total'):,} total ({token_counts.get('input'):,} in / {token_counts.get('output'):,} out)"
                
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
