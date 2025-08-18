"""
Demo script to showcase dynamic prompting capabilities with the NCERT RAG Assistant.
This script makes direct API calls to compare how the system responds to different question types.
"""

import requests
import json
import time
from rich.console import Console
from rich.markdown import Markdown
from rich import print as rprint

# Configuration
API_URL = "http://localhost:8080/ask"
console = Console()

# Sample questions categorized by question type
QUESTIONS = {
    "Definition": {
        "question": "What is Newton's Third Law of Motion?",
        "subject": "Physics"
    },
    "Comparison": {
        "question": "Compare mitosis and meiosis.",
        "subject": "Biology"
    },
    "Process": {
        "question": "Explain the process of DNA replication.",
        "subject": "Biology"
    },
    "Problem Solving": {
        "question": "Solve the definite integral of x² from 0 to 2.",
        "subject": "Math"
    },
    "Application": {
        "question": "What are the practical applications of logarithms?",
        "subject": "Math"
    }
}

def make_api_request(question, subject, use_dynamic=True):
    """Make API request to the backend with specified parameters."""
    payload = {
        "question": question,
        "subject": subject,
        "temperature": 0.2,  # Fixed temperature for consistency
        "use_dynamic": use_dynamic
    }
    
    try:
        response = requests.post(
            API_URL, 
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        return response.json()
    except requests.exceptions.ConnectionError:
        console.print("[bold red]Error: Cannot connect to the backend API. Make sure the backend server is running.[/]")
        return None
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/]")
        return None

def demonstrate_question_type(question_type):
    """Show how dynamic prompting handles a specific question type."""
    question_data = QUESTIONS[question_type]
    question = question_data["question"]
    subject = question_data["subject"]
    
    console.rule(f"[bold blue]Question Type: {question_type}[/]")
    console.print(f"[bold cyan]Subject:[/] {subject}")
    console.print(f"[bold cyan]Question:[/] {question}\n")
    
    # Get response with dynamic prompting
    console.print("[bold yellow]Getting response with dynamic prompting...[/]")
    start_time = time.time()
    dynamic_response = make_api_request(question, subject, use_dynamic=True)
    dynamic_time = time.time() - start_time
    
    if not dynamic_response:
        return
    
    # Get response without dynamic prompting
    console.print("[bold yellow]Getting response without dynamic prompting...[/]")
    start_time = time.time()
    standard_response = make_api_request(question, subject, use_dynamic=False)
    standard_time = time.time() - start_time
    
    if not standard_response:
        return
    
    # Display results
    console.rule("[bold green]WITH Dynamic Prompting[/]")
    console.print(Markdown(dynamic_response.get("answer", "No answer received")))
    console.print(f"[dim]Response time: {dynamic_time:.2f}s | Detected as: {dynamic_response.get('question_type', 'unknown')}[/]")
    
    console.rule("[bold green]WITHOUT Dynamic Prompting[/]")
    console.print(Markdown(standard_response.get("answer", "No answer received")))
    console.print(f"[dim]Response time: {standard_time:.2f}s[/]")
    
    console.rule()

def main():
    """Run the demonstration."""
    console.print("[bold magenta]Dynamic Prompting Demonstration[/]")
    console.print("This script compares responses with and without dynamic prompting for different question types.\n")
    
    for question_type in QUESTIONS.keys():
        demonstrate_question_type(question_type)
        if question_type != list(QUESTIONS.keys())[-1]:
            console.print("\nPress Enter to continue to the next question type...", end="")
            input()
        
    console.print("[bold green]Demonstration completed![/]")

if __name__ == "__main__":
    main()
