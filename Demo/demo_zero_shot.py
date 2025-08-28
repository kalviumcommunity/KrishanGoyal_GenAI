"""
Demo script for zero-shot prompting in the educational Q&A system.

This script demonstrates how the system answers questions without using example Q&A pairs,
relying only on clear instructions about how to format the response.
"""

import requests
import sys
import time

# For local development we use this URL
API_URL = "http://localhost:8080/ask"

# Set of demonstration questions for various subjects
DEMO_QUESTIONS = [
    {
        "subject": "Physics",
        "question": "Explain Guass's Law."
    },
    {
        "subject": "Biology",
        "question": "Describe the process of meiosis and its significance in reproduction."
    },
    {
        "subject": "Math",
        "question": "What are the properties and applications of the definite integral?"
    }
]

def run_demo():
    """Run the zero-shot prompting demonstration."""
    
    print("\n🔍 Zero-Shot Prompting Demonstration")
    print("====================================")
    print("This demo shows how our system can answer educational questions")
    print("using zero-shot prompting - without example Q&A pairs to guide the format.\n")
    
    for i, demo in enumerate(DEMO_QUESTIONS, 1):
        subject = demo["subject"]
        question = demo["question"]
        
        print(f"\n✨ Demo {i}: {subject} Question")
        print(f"Question: {question}")
        print("\nThinking...", end="", flush=True)
        
        try:
            # Make API request with zero-shot prompting enabled
            response = requests.post(
                API_URL,
                json={
                    "question": question,
                    "subject": subject,
                    "temperature": 0.2,
                    "use_zero_shot": True,
                    "use_one_shot": False,
                    "use_multi_shot": False,
                    "use_dynamic": False
                },
                headers={"Content-Type": "application/json"}
            )
            
            # Simple progress indicator
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.3)
            
            if response.status_code == 200:
                result = response.json()
                
                # Clear the "Thinking..." text
                print("\r" + " " * 20 + "\r", end="")
                
                print("\n📝 Answer:\n")
                # Print the answer with proper formatting
                print(result.get("answer", "No answer received"))
                
                # Show metadata about the response
                print("\n🔧 Response metadata:")
                print(f"- Temperature: {result.get('temperature')}")
                print(f"- Retrieved contexts: {result.get('used_k')}")
                print(f"- Zero-shot prompting: {result.get('used_zero_shot')}")
                print("-" * 60)
                
                # Add a pause between questions
                if i < len(DEMO_QUESTIONS):
                    input("\nPress Enter for next demo question...")
                
            else:
                print(f"\nError: {response.status_code} - {response.text}")
        
        except requests.exceptions.ConnectionError:
            print("\n❌ Cannot connect to backend server. Please make sure the backend is running.")
            print("   Run the server using: python -m backend.app.main")
            sys.exit(1)
    
    print("\n✅ Demo complete!")
    print("Zero-shot prompting relies solely on clear instructions without examples.")
    print("It's effective when the model already knows the preferred format or when")
    print("the instructions are clear enough to guide the response structure.")

if __name__ == "__main__":
    run_demo()
