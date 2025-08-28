"""
Demo script for token usage comparison in the educational Q&A system.

This script demonstrates token usage across different prompting techniques:
- Zero-shot
- One-shot
- Multi-shot
- Dynamic

It helps analyze the efficiency and performance of different prompting strategies.
"""

import requests
import sys
import time
import json
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich import print as rprint

# For local development we use this URL
API_URL = "http://localhost:8080/ask"
console = Console()

# Set of test questions for token usage comparison
TEST_QUESTIONS = [
    {
        "subject": "Physics",
        "question": "Explain the principle of superposition in waves."
    },
    {
        "subject": "Biology",
        "question": "Describe the process of DNA replication."
    },
    {
        "subject": "Math",
        "question": "What is integration by parts and when is it used?"
    }
]

# Prompting techniques to test
PROMPTING_TECHNIQUES = [
    {
        "name": "Zero-Shot",
        "params": {
            "use_zero_shot": True,
            "use_one_shot": False,
            "use_multi_shot": False,
            "use_dynamic": False,
            "use_chain_of_thought": False
        }
    },
    {
        "name": "One-Shot",
        "params": {
            "use_zero_shot": False,
            "use_one_shot": True,
            "use_multi_shot": False,
            "use_dynamic": False,
            "use_chain_of_thought": False
        }
    },
    {
        "name": "Multi-Shot",
        "params": {
            "use_zero_shot": False,
            "use_one_shot": False,
            "use_multi_shot": True,
            "use_dynamic": False,
            "use_chain_of_thought": False
        }
    },
    {
        "name": "Dynamic",
        "params": {
            "use_zero_shot": False,
            "use_one_shot": False,
            "use_multi_shot": False,
            "use_dynamic": True,
            "use_chain_of_thought": False
        }
    },
    {
        "name": "Chain-of-Thought",
        "params": {
            "use_zero_shot": False,
            "use_one_shot": False,
            "use_multi_shot": False,
            "use_dynamic": False,
            "use_chain_of_thought": True
        }
    }
]

def make_api_request(question, subject, technique_params):
    """Make API request with specified parameters."""
    try:
        payload = {
            "question": question,
            "subject": subject,
            "temperature": 0.2,
            **technique_params
        }
        
        console.print(f"  [dim]Sending request with params: {technique_params}[/]", end="")
        
        response = requests.post(
            API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60  # Increased timeout to 60 seconds
        )
        
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                console.print(f"[bold red] Error: Invalid JSON in response[/]")
                console.print(f"[dim]Response text: {response.text[:100]}...[/]")
                return None
        else:
            console.print(f"[bold red] Error: {response.status_code} - {response.text[:100]}[/]")
            return None
            
    except requests.exceptions.ConnectionError:
        console.print("[bold red] Cannot connect to backend server. Please make sure the backend is running.[/]")
        return None
    except requests.exceptions.Timeout:
        console.print("[bold red] Request timed out. The server might be overloaded.[/]")
        return None
    except Exception as e:
        console.print(f"[bold red] Unexpected error: {str(e)}[/]")
        return None

def run_token_usage_test():
    """Run the token usage comparison tests."""
    
    console.rule("[bold blue]Token Usage Comparison Test[/]")
    console.print("Comparing token usage across different prompting techniques...\n")
    
    results = []
    
    # Process each test question
    for test_case in TEST_QUESTIONS:
        subject = test_case["subject"]
        question = test_case["question"]
        
        console.print(f"[bold cyan]Testing: {subject} question[/]")
        console.print(f"Question: {question}")
        
        technique_results = []
        
        # Test each prompting technique
        for technique in PROMPTING_TECHNIQUES:
            technique_name = technique["name"]
            params = technique["params"]
            
            console.print(f"  [yellow]Testing {technique_name} prompting...[/]")
            
            start_time = time.time()
            response = make_api_request(question, subject, params)
            elapsed_time = time.time() - start_time
            
            if response:
                # Check if token counts are available
                if "token_counts" in response:
                    tokens = response["token_counts"]
                    model = tokens.get("model", "unknown")
                    console.print(f"  [green]Success! ({tokens.get('total', 0)} tokens in {elapsed_time:.2f}s, model: {model})[/]")
                    
                    technique_results.append({
                        "technique": technique_name,
                        "input_tokens": tokens.get("input", 0),
                        "output_tokens": tokens.get("output", 0),
                        "total_tokens": tokens.get("total", 0),
                        "model": model,
                        "response_time": elapsed_time
                    })
                else:
                    # If we have a response but no token counts, create estimated counts
                    answer = response.get("answer", "")
                    estimated_input_tokens = len(question.split()) * 2  # Rough estimate
                    estimated_output_tokens = len(answer.split())
                    estimated_total = estimated_input_tokens + estimated_output_tokens
                    
                    console.print(f"  [yellow]Success but no token data. (Est: ~{estimated_total} tokens in {elapsed_time:.2f}s)[/]")
                    
                    technique_results.append({
                        "technique": technique_name,
                        "input_tokens": estimated_input_tokens,
                        "output_tokens": estimated_output_tokens,
                        "total_tokens": estimated_total,
                        "model": "unknown",
                        "response_time": elapsed_time,
                        "estimated": True
                    })
            else:
                console.print(f"  [bold red]Failed! Could not get a valid response.[/]")
        
        results.append({
            "subject": subject,
            "question": question,
            "results": technique_results
        })
        
        console.print()
    
    # Display results in tables
    display_results(results)
    
    # Save results to a JSON file
    with open("token_usage_results.json", "w") as f:
        json.dump(results, f, indent=2)
    console.print("[green]Results saved to token_usage_results.json[/]")

def display_results(results):
    """Display test results in formatted tables."""
    
    console.rule("[bold green]Token Usage Results Summary[/]")
    
    # Create a summary table across all questions
    summary_table = Table(title="Average Token Usage by Technique")
    summary_table.add_column("Technique", style="cyan")
    summary_table.add_column("Input Tokens", justify="right")
    summary_table.add_column("Output Tokens", justify="right")
    summary_table.add_column("Total Tokens", justify="right", style="bold")
    summary_table.add_column("Model", justify="left")
    summary_table.add_column("Response Time", justify="right")
    
    # Calculate averages
    technique_totals = {}
    technique_counts = {}
    
    for test_case in results:
        for result in test_case["results"]:
            technique = result["technique"]
            
            if technique not in technique_totals:
                technique_totals[technique] = {
                    "input": 0,
                    "output": 0, 
                    "total": 0,
                    "time": 0,
                    "models": set()
                }
                technique_counts[technique] = 0
                
            technique_totals[technique]["input"] += result["input_tokens"]
            technique_totals[technique]["output"] += result["output_tokens"]
            technique_totals[technique]["total"] += result["total_tokens"]
            technique_totals[technique]["time"] += result["response_time"]
            technique_totals[technique]["models"].add(result.get("model", "unknown"))
            technique_counts[technique] += 1
    
    # Add rows to summary table
    for technique in PROMPTING_TECHNIQUES:
        name = technique["name"]
        if name in technique_totals:
            count = technique_counts[name]
            avg_input = int(technique_totals[name]["input"] / count)
            avg_output = int(technique_totals[name]["output"] / count)
            avg_total = int(technique_totals[name]["total"] / count)
            avg_time = technique_totals[name]["time"] / count
            
            # Check if any results were estimated
            has_estimated = any(result.get("estimated", False) 
                              for test_case in results 
                              for result in test_case["results"] 
                              if result["technique"] == name)
            
            row_style = "dim" if has_estimated else None
            
            # Join the model names with commas
            models_str = ", ".join(sorted(technique_totals[name]["models"]))
            
            summary_table.add_row(
                name,
                f"{avg_input:,}",
                f"{avg_output:,}",
                f"{avg_total:,}",
                models_str,
                f"{avg_time:.2f}s",
                style=row_style
            )
            
            if has_estimated:
                summary_table.caption = "* Some values are estimates due to missing token data"
    
    console.print(summary_table)
    
    # Display detailed results for each question
    for test_case in results:
        console.rule(f"[bold blue]Results for {test_case['subject']} Question[/]")
        console.print(f"[bold]Question:[/] {test_case['question']}\n")
        
        detail_table = Table()
        detail_table.add_column("Technique", style="cyan")
        detail_table.add_column("Model", justify="left")
        detail_table.add_column("Input Tokens", justify="right")
        detail_table.add_column("Output Tokens", justify="right")
        detail_table.add_column("Total Tokens", justify="right", style="bold")
        detail_table.add_column("Response Time", justify="right")
        
        for result in test_case["results"]:
            row_style = "dim" if result.get("estimated", False) else None
            
            # Add an asterisk to estimated values
            suffix = "*" if result.get("estimated", False) else ""
            
            detail_table.add_row(
                result["technique"],
                result.get("model", "unknown"),
                f"{result['input_tokens']:,}{suffix}",
                f"{result['output_tokens']:,}{suffix}",
                f"{result['total_tokens']:,}{suffix}",
                f"{result['response_time']:.2f}s",
                style=row_style
            )
            
        if any(result.get("estimated", False) for result in test_case["results"]):
            detail_table.caption = "* Estimated values due to missing token data"
            
        console.print(detail_table)
        console.print()

if __name__ == "__main__":
    try:
        run_token_usage_test()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Test interrupted by user.[/]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/]")
        sys.exit(1)
