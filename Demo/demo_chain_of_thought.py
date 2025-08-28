"""
Demo script to showcase Chain of Thought (CoT) prompting capabilities with the NCERT RAG Assistant.
This script makes direct API calls to compare how Chain of Thought impacts responses for complex reasoning tasks.
"""

import requests
import sys
import time
import json
from rich.console import Console
from rich.markdown import Markdown
from rich import print as rprint
from rich.panel import Panel
from rich.table import Table

# Configuration
API_URL = "http://localhost:8080/ask"
console = Console()

# Sample questions that benefit from step-by-step reasoning
QUESTIONS = {
    "Mathematics": {
        "question": "A cylindrical tank with a radius of 5 meters is being filled with water at a rate of 3 cubic meters per minute. Find the rate at which the height of the water in the tank is increasing.",
        "subject": "Math"
    },
    "Physics": {
        "question": "A 5kg object falls from a height of 20m. Calculate its kinetic energy just before hitting the ground.",
        "subject": "Physics"
    },
    "Chemistry": {
        "question": "Describe the process of fertilization in humans. Where does it occur, and what are the key steps involved?",
        "subject": "Biology"
    },
    "Logic": {
        "question": "If all A are B, and some B are C, what can we conclude about the relationship between A and C?",
        "subject": "Logic"
    }
}

def make_api_request(question, subject, use_cot=False):
    """Make API request to the backend with specified parameters."""
    
    payload = {
        "question": question,
        "subject": subject,
        "temperature": 0.2,
        "use_chain_of_thought": use_cot  # Our backend now supports this parameter
    }
    
    try:
        console.print(f"Sending request for {'CoT' if use_cot else 'standard'} response...", end="")
        
        response = requests.post(
            API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60  # Increased timeout to 60 seconds
        )
        
        if response.status_code == 200:
            console.print(" [green]Success![/]")
            try:
                return response.json()
            except json.JSONDecodeError:
                console.print(f"[bold red]Error: Invalid JSON in response[/]")
                return None
        else:
            console.print(f"[bold red] Error: {response.status_code}[/]")
            return None
            
    except requests.exceptions.ConnectionError:
        console.print("[bold red]Cannot connect to backend server. Please make sure the backend is running.[/]")
        # For demo purposes, we'll return a simulated response if the server is not available
        return get_simulated_response(question, subject, use_cot)
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {str(e)}[/]")
        # For demo purposes, we'll return a simulated response if there's an error
        return get_simulated_response(question, subject, use_cot)

def get_simulated_response(question, subject, use_cot):
    """Generate a simulated response for demonstration purposes."""
    if "integral of x^2 * ln(x)" in question:
        if use_cot:
            return {
                "answer": """# Solving the integral of x^2 * ln(x) dx

I'll tackle this step by step using integration by parts.

## Step 1: Identify the parts for integration by parts
Using the formula ∫u(x)v'(x)dx = u(x)v(x) - ∫v(x)u'(x)dx

Let:
- u(x) = ln(x)
- v'(x) = x²

## Step 2: Calculate the derivatives and integrals
- u(x) = ln(x)
- u'(x) = 1/x
- v'(x) = x²
- v(x) = ∫x²dx = x³/3

## Step 3: Apply the integration by parts formula
∫x² ln(x) dx = ln(x) · (x³/3) - ∫(x³/3) · (1/x) dx
= (x³ ln(x))/3 - ∫x²/3 dx
= (x³ ln(x))/3 - (x³/9) + C

## Step 4: Simplify the final expression
∫x² ln(x) dx = (x³ ln(x))/3 - x³/9 + C
= (x³/3)(ln(x) - 1/3) + C

Therefore, ∫x² ln(x) dx = (x³ ln(x))/3 - x³/9 + C
""",
                "token_counts": {"input": 135, "output": 312, "total": 447, "model": "mock-gemini-model"}
            }
        else:
            return {
                "answer": """# Integral of x² ln(x)

The solution is:
∫x² ln(x) dx = (x³ ln(x))/3 - x³/9 + C

This can be solved using integration by parts with u = ln(x) and dv = x²dx.
""",
                "token_counts": {"input": 65, "output": 112, "total": 177, "model": "mock-gemini-model"}
            }
    elif "5kg object falls from a height of 20m" in question:
        if use_cot:
            return {
                "answer": """# Calculating Kinetic Energy of a Falling Object

I'll calculate the kinetic energy of a 5kg object falling from 20m height just before hitting the ground.

## Step 1: Identify the relevant physics principles
When an object falls, gravitational potential energy converts to kinetic energy.
If we ignore air resistance, mechanical energy is conserved.

## Step 2: Write the conservation of energy equation
Initial potential energy = Final kinetic energy
mgh = (1/2)mv²

Where:
- m = mass of the object (5 kg)
- g = acceleration due to gravity (9.8 m/s²)
- h = height (20 m)
- v = final velocity

## Step 3: Calculate the final velocity using energy conservation
mgh = (1/2)mv²
gh = (1/2)v²
v² = 2gh
v² = 2 × 9.8 × 20
v² = 392
v = √392 ≈ 19.8 m/s

## Step 4: Calculate the kinetic energy
KE = (1/2)mv²
KE = (1/2) × 5 × 392
KE = 2.5 × 392
KE = 980 J

Therefore, the kinetic energy just before hitting the ground is 980 joules.
""",
                "token_counts": {"input": 142, "output": 390, "total": 532, "model": "mock-gemini-model"}
            }
        else:
            return {
                "answer": """# Kinetic Energy Calculation

The kinetic energy of the 5kg object just before hitting the ground is 980 joules.

This is calculated using the principle of conservation of energy, where the initial potential energy (mgh) equals the final kinetic energy (1/2 × m × v²).
""",
                "token_counts": {"input": 75, "output": 120, "total": 195, "model": "mock-gemini-model"}
            }
    elif "Balance the chemical equation" in question:
        if use_cot:
            return {
                "answer": """# Balancing Fe + O₂ → Fe₂O₃

I'll balance this chemical equation step by step.

## Step 1: Write the unbalanced equation with elements identified
Fe + O₂ → Fe₂O₃

Elements present:
- Fe (Iron): 1 atom on left, 2 atoms on right
- O (Oxygen): 2 atoms on left, 3 atoms on right

## Step 2: Balance iron (Fe) first
To get 2 Fe atoms on the left to match the right:
2Fe + O₂ → Fe₂O₃

Elements now:
- Fe: 2 atoms on left, 2 atoms on right ✓
- O: 2 atoms on left, 3 atoms on right ✗

## Step 3: Balance oxygen (O)
We need 3 oxygen atoms on the left to match the right.
But we have O₂ molecules, so we need 3/2 of them.
Multiply everything by 2 to get whole numbers:
4Fe + 3O₂ → 2Fe₂O₃

Let's check:
- Fe: 4 atoms on left, 4 atoms on right (2×2) ✓
- O: 6 atoms on left (3×2), 6 atoms on right (2×3) ✓

## Step 4: Verify the balanced equation
4Fe + 3O₂ → 2Fe₂O₃

Both sides have the same number of each type of atom, so the equation is balanced.

Therefore, the balanced chemical equation is 4Fe + 3O₂ → 2Fe₂O₃
""",
                "token_counts": {"input": 125, "output": 370, "total": 495, "model": "mock-gemini-model"}
            }
        else:
            return {
                "answer": """# Balanced Chemical Equation

The balanced chemical equation is:
4Fe + 3O₂ → 2Fe₂O₃

This ensures equal numbers of iron and oxygen atoms on both sides of the equation.
""",
                "token_counts": {"input": 70, "output": 105, "total": 175, "model": "mock-gemini-model"}
            }
    else:
        if use_cot:
            return {
                "answer": """# Analyzing the Logical Relationship

I'll analyze this logical problem step by step.

## Step 1: Understand the given statements
1. All A are B
2. Some B are C

## Step 2: Represent the first statement "All A are B"
This means every element in set A is also in set B.
A is a subset of B.

## Step 3: Represent the second statement "Some B are C"
This means there is at least one element in set B that is also in set C.
The intersection of B and C is not empty: B ∩ C ≠ ∅

## Step 4: Analyze the possible relationships between A and C
There are two possibilities:

Possibility 1: The elements of B that overlap with C include some elements of A.
In this case, some A are C.

Possibility 2: The elements of B that overlap with C don't include any elements of A.
In this case, no A are C.

## Step 5: Draw a conclusion
Since both possibilities are valid based on the given information, we cannot make a definitive conclusion about the relationship between A and C.

Therefore, from the statements "All A are B" and "Some B are C," we cannot conclude anything definitive about the relationship between A and C. Both "Some A are C" and "No A are C" remain possible.
""",
                "token_counts": {"input": 130, "output": 410, "total": 540, "model": "mock-gemini-model"}
            }
        else:
            return {
                "answer": """# Logical Relationship Analysis

From the statements "All A are B" and "Some B are C," we cannot make a definitive conclusion about the relationship between A and C.

Both of these scenarios are possible:
- Some A are C
- No A are C

The information provided is insufficient to determine which of these is true.
""",
                "token_counts": {"input": 70, "output": 130, "total": 200, "model": "mock-gemini-model"}
            }

def compare_responses(problem_type):
    """Compare standard and Chain of Thought responses for a problem."""
    question_data = QUESTIONS[problem_type]
    question = question_data["question"]
    subject = question_data["subject"]
    
    console.rule(f"[bold blue]{problem_type} Problem[/]")
    console.print(f"[bold cyan]Question:[/] {question}\n")
    
    # Get standard response
    console.print("[bold yellow]Getting standard response...[/]")
    start_time = time.time()
    standard_response = make_api_request(question, subject, use_cot=False)
    standard_time = time.time() - start_time
    
    if not standard_response:
        console.print("[bold red]Failed to get standard response.[/]")
        return
    
    # Get Chain of Thought response
    console.print("\n[bold yellow]Getting Chain of Thought response...[/]")
    start_time = time.time()
    cot_response = make_api_request(question, subject, use_cot=True)
    cot_time = time.time() - start_time
    
    if not cot_response:
        console.print("[bold red]Failed to get Chain of Thought response.[/]")
        return
    
    # Compare token usage
    std_tokens = standard_response.get("token_counts", {"total": "unknown"})
    cot_tokens = cot_response.get("token_counts", {"total": "unknown"})
    
    # Display token comparison
    token_table = Table(title="Token Usage Comparison")
    token_table.add_column("Approach", style="cyan")
    token_table.add_column("Input Tokens", justify="right")
    token_table.add_column("Output Tokens", justify="right")
    token_table.add_column("Total Tokens", justify="right", style="bold")
    token_table.add_column("Response Time", justify="right")
    
    token_table.add_row(
        "Standard",
        f"{std_tokens.get('input', 'unknown')}",
        f"{std_tokens.get('output', 'unknown')}",
        f"{std_tokens.get('total', 'unknown')}",
        f"{standard_time:.2f}s"
    )
    
    token_table.add_row(
        "Chain of Thought",
        f"{cot_tokens.get('input', 'unknown')}",
        f"{cot_tokens.get('output', 'unknown')}",
        f"{cot_tokens.get('total', 'unknown')}",
        f"{cot_time:.2f}s"
    )
    
    console.print("\n")
    console.print(token_table)
    
    # Display the standard answer
    console.rule("[bold green]Standard Response[/]")
    console.print(Markdown(standard_response["answer"]))
    
    # Display the Chain of Thought answer
    console.rule("[bold green]Chain of Thought Response[/]")
    console.print(Markdown(cot_response["answer"]))
    
    # Display insight about the difference
    console.rule("[bold magenta]Key Insight[/]")
    
    # Calculate length difference percentage
    std_length = len(standard_response["answer"])
    cot_length = len(cot_response["answer"])
    length_diff_pct = (cot_length - std_length) / std_length * 100
    
    # Calculate token count difference percentage
    if isinstance(std_tokens.get('total'), int) and isinstance(cot_tokens.get('total'), int):
        token_diff_pct = (cot_tokens['total'] - std_tokens['total']) / std_tokens['total'] * 100
        token_diff_msg = f"{token_diff_pct:.1f}% more tokens"
    else:
        token_diff_msg = "unknown token difference"
    
    insight = f"""Chain of Thought prompting generated a response that is:
- {length_diff_pct:.1f}% longer than the standard response
- Shows {token_diff_msg}
- Includes detailed reasoning steps, intermediate calculations, and explicit logical connections
- Makes the problem-solving process transparent and educational
"""
    
    console.print(Panel(insight, title="Comparison Results"))
    console.print()

def main():
    """Demonstrate Chain of Thought prompting with various problem types."""
    console.rule("[bold blue]Chain of Thought (CoT) Prompting Demonstration[/]")
    console.print("""Chain of Thought prompting encourages the model to show its step-by-step reasoning process,
making complex problem-solving more transparent and often more accurate.
    
This demo compares standard responses with Chain of Thought responses for different problem types.
""")
    
    # Run comparisons for all problem types
    for problem_type in QUESTIONS:
        compare_responses(problem_type)
        # Pause between problems for better readability
        time.sleep(1)
    
    console.rule("[bold blue]Demonstration Complete[/]")
    console.print("""
Chain of Thought prompting is most beneficial for problems that involve:
- Multi-step reasoning
- Mathematical calculations
- Logical deduction
- Scientific analysis
- Step-by-step procedures

It typically uses more tokens but provides more educational, transparent responses.
""")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Demonstration interrupted by user.[/]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/]")
        sys.exit(1)
