"""
Demo script to showcase multi-shot prompting capabilities with the NCERT RAG Assistant.
This script makes direct API calls to compare responses with one-shot and multi-shot prompting.
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
    "Physics": "Explain the principle of superposition in waves",
    "Biology": "Describe the process of meiosis and its significance",
    "Math": "Explain the concept of limits in calculus"
}

def make_api_request(question, subject, use_one_shot=False, use_multi_shot=False):
    """Make API request to the backend with specified parameters."""
    payload = {
        "question": question,
        "subject": subject,
        "temperature": 0.2,  # Fixed temperature for consistency
        "use_one_shot": use_one_shot,
        "use_multi_shot": use_multi_shot
    }
    
    try:
        response = requests.post(
            API_URL, 
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=60  # Longer timeout since multi-shot responses can take more time
        )
        return response.json()
    except requests.exceptions.ConnectionError:
        console.print("[bold red]Error: Cannot connect to the backend API. Make sure the backend server is running.[/]")
        return None
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/]")
        return None

def compare_responses(subject):
    """Compare responses with one-shot and multi-shot prompting for a subject."""
    question = QUESTIONS[subject]
    
    console.rule(f"[bold blue]Subject: {subject}[/]")
    console.print(f"[bold cyan]Question:[/] {question}\n")
    
    # Standard response (no examples)
    console.print("[bold yellow]Getting standard response (no examples)...[/]")
    start_time = time.time()
    standard_response = make_api_request(question, subject)
    standard_time = time.time() - start_time
    
    if not standard_response:
        return
        
    # One-shot response
    console.print("[bold yellow]Getting response with ONE-SHOT prompting...[/]")
    start_time = time.time()
    one_shot_response = make_api_request(question, subject, use_one_shot=True)
    one_shot_time = time.time() - start_time
    
    if not one_shot_response:
        return
    
    # Multi-shot response
    console.print("[bold yellow]Getting response with MULTI-SHOT prompting...[/]")
    start_time = time.time()
    multi_shot_response = make_api_request(question, subject, use_multi_shot=True)
    multi_shot_time = time.time() - start_time
    
    if not multi_shot_response:
        return
    
    # Display results
    console.rule("[bold green]WITHOUT Any Examples[/]")
    console.print(Markdown(standard_response.get("answer", "No answer received")))
    console.print(f"[dim]Response time: {standard_time:.2f}s[/]")
    
    console.rule("[bold green]WITH One-Shot Example[/]")
    console.print(Markdown(one_shot_response.get("answer", "No answer received")))
    console.print(f"[dim]Response time: {one_shot_time:.2f}s[/]")
    
    console.rule("[bold green]WITH Multi-Shot Examples[/]")
    console.print(Markdown(multi_shot_response.get("answer", "No answer received")))
    console.print(f"[dim]Response time: {multi_shot_time:.2f}s[/]")
    
    console.rule()

def main():
    """Run the demonstration."""
    console.print("[bold magenta]Multi-Shot Prompting Demonstration[/]")
    console.print("This script compares responses with no examples, one-shot, and multi-shot prompting.\n")
    
    for subject in QUESTIONS.keys():
        compare_responses(subject)
        if subject != list(QUESTIONS.keys())[-1]:
            console.print("\nPress Enter to continue to the next subject...", end="")
            input()
        
    console.print("[bold green]Demonstration completed![/]")

if __name__ == "__main__":
    main()
