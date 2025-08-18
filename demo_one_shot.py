"""
Demo script to showcase one-shot prompting capabilities with the NCERT RAG Assistant.
This script makes direct API calls to compare responses with and without one-shot prompting.
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

# Sample questions for different subjects
QUESTIONS = {
    "Physics": "Explain the principle of superposition in waves"
}

def make_api_request(question, subject, use_one_shot=False):
    """Make API request to the backend with specified parameters."""
    payload = {
        "question": question,
        "subject": subject,
        "temperature": 0.2,  # Fixed temperature for consistency
        "use_one_shot": use_one_shot
    }
    
    try:
        response = requests.post(
            API_URL, 
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30  # Longer timeout since LLM responses can take time
        )
        return response.json()
    except requests.exceptions.ConnectionError:
        console.print("[bold red]Error: Cannot connect to the backend API. Make sure the backend server is running.[/]")
        return None
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/]")
        return None

def compare_responses(subject):
    """Compare responses with and without one-shot prompting for a subject."""
    question = QUESTIONS[subject]
    
    console.rule(f"[bold blue]Subject: {subject}[/]")
    console.print(f"[bold cyan]Question:[/] {question}\n")
    
    # Without one-shot
    console.print("[bold yellow]Getting response WITHOUT one-shot prompting...[/]")
    start_time = time.time()
    regular_response = make_api_request(question, subject, use_one_shot=False)
    regular_time = time.time() - start_time
    
    if not regular_response:
        return
        
    # With one-shot
    console.print("[bold yellow]Getting response WITH one-shot prompting...[/]")
    start_time = time.time()
    one_shot_response = make_api_request(question, subject, use_one_shot=True)
    one_shot_time = time.time() - start_time
    
    if not one_shot_response:
        return
    
    # Display results
    console.rule("[bold green]WITHOUT One-Shot Prompting[/]")
    console.print(Markdown(regular_response.get("answer", "No answer received")))
    console.print(f"[dim]Response time: {regular_time:.2f}s[/]")
    
    console.rule("[bold green]WITH One-Shot Prompting[/]")
    console.print(Markdown(one_shot_response.get("answer", "No answer received")))
    console.print(f"[dim]Response time: {one_shot_time:.2f}s[/]")
    
    console.rule()

def main():
    """Run the demonstration."""
    console.print("[bold magenta]One-Shot Prompting Demonstration[/]")
    console.print("This script compares responses with and without one-shot prompting.\n")
    
    for subject in QUESTIONS.keys():
        compare_responses(subject)
        console.print("\nPress Enter to continue to the next subject...", end="")
        input()
        
    console.print("[bold green]Demonstration completed![/]")

if __name__ == "__main__":
    main()
