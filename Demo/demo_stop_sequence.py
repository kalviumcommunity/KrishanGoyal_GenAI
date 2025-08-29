"""
Demo script for stop sequence usage in the educational Q&A system.

This script demonstrates how to use the stop sequence parameter in LLM API calls
to control where the model should stop generating output.

It compares responses with and without a stop sequence for educational questions.
"""

import requests
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich import print as rprint
import time
import random

# For demo purposes, we'll use a mock implementation since we're having server connection issues
API_URL = "http://localhost:8080/ask"
console = Console()

TEST_QUESTIONS = [
    {
        "subject": "Physics",
        "question": "Explain the law of conservation of energy."
    },
    {
        "subject": "Math",
        "question": "What is the quadratic formula?"
    }
]

STOP_SEQUENCE = "\n---END---"

# Mock responses for demo purposes
MOCK_RESPONSES = {
    "conservation of energy": """# Law of Conservation of Energy

The law of conservation of energy states that energy cannot be created or destroyed, only transformed from one form to another or transferred from one object to another.

## Key Points:
* Total energy in an isolated system remains constant
* Energy can change forms (kinetic, potential, thermal, etc.)
* In all physical and chemical processes, energy is conserved

## Mathematical Expression:
E_initial = E_final

## Applications:
1. Analyzing mechanical systems like pendulums
2. Understanding thermal processes and heat transfer
3. Explaining chemical reactions and their energy changes
4. Nuclear physics and radioactive decay

---END---

The law has broad implications across all fields of physics and forms one of the fundamental principles of modern science.""",

    "quadratic formula": """# The Quadratic Formula

The quadratic formula is used to solve quadratic equations of the form ax² + bx + c = 0.

## Formula:
x = [-b ± √(b² - 4ac)] / 2a

## Components:
* a, b, c are coefficients in the quadratic equation
* ± indicates there are typically two solutions
* b² - 4ac is called the discriminant

## Discriminant Analysis:
* If b² - 4ac > 0: Two distinct real solutions
* If b² - 4ac = 0: One real solution (repeated root)
* If b² - 4ac < 0: Two complex solutions

---END---

## Historical Context:
The quadratic formula has been known in various forms since ancient times, with contributions from Babylonian, Greek, Indian, and Islamic mathematicians."""
}


def make_api_request(question, subject, stop_sequence=None):
    """Simulated API request with mock responses."""
    # Simulate network delay
    start = time.time()
    time.sleep(random.uniform(0.5, 1.5))
    elapsed = time.time() - start
    
    # Determine which mock response to use
    if "conservation" in question.lower():
        response = MOCK_RESPONSES["conservation of energy"]
    elif "quadratic" in question.lower():
        response = MOCK_RESPONSES["quadratic formula"]
    else:
        response = "Mock response not available for this question."
    
    # Apply stop sequence if provided
    if stop_sequence and stop_sequence in response:
        response = response.split(stop_sequence)[0]
    
    # Generate mock token counts
    input_tokens = len(question.split()) + 20
    output_tokens = len(response.split())
    total_tokens = input_tokens + output_tokens
    
    token_counts = {
        "input": input_tokens,
        "output": output_tokens,
        "total": total_tokens,
        "model": "mock-model"
    }
    
    return response, token_counts, elapsed


def main():
    console.rule("[bold green]Stop Sequence Prompting Demonstration")
    rprint("[bold]This demo shows how using a stop sequence can control the output of the LLM.[/bold]\n")
    for q in TEST_QUESTIONS:
        console.rule(f"[bold blue]{q['subject']} Question")
        rprint(f"[bold]Question:[/bold] {q['question']}")
        # Standard response
        rprint("\n[bold]Getting standard response...[/bold]")
        answer_std, tokens_std, t_std = make_api_request(q["question"], q["subject"])
        # With stop sequence
        rprint("[bold]Getting response with stop sequence...[/bold]")
        answer_stop, tokens_stop, t_stop = make_api_request(q["question"], q["subject"], STOP_SEQUENCE)

        table = Table(title="Token Usage Comparison")
        table.add_column("Approach")
        table.add_column("Input Tokens")
        table.add_column("Output Tokens")
        table.add_column("Total Tokens")
        table.add_column("Response Time")
        table.add_row("Standard", str(tokens_std.get("input", "-")), str(tokens_std.get("output", "-")), str(tokens_std.get("total", "-")), f"{t_std:.2f}s")
        table.add_row("With Stop Sequence", str(tokens_stop.get("input", "-")), str(tokens_stop.get("output", "-")), str(tokens_stop.get("total", "-")), f"{t_stop:.2f}s")
        console.print(table)

        rprint("[bold]Standard Response:[/bold]")
        rprint(Markdown(answer_std))
        rprint("[bold]Response with Stop Sequence:[/bold]")
        rprint(Markdown(answer_stop))
        console.rule()

if __name__ == "__main__":
    main()
