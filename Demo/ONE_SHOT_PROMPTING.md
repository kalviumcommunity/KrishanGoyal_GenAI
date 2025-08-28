# One-Shot Prompting Guide

## What is One-Shot Prompting?

One-shot prompting is a technique where we provide the language model with a single example of the desired input-output format before asking it to respond to a new question. This helps guide the model to produce responses in a consistent style and format.

## Benefits of One-Shot Prompting

- **Consistent Format**: Responses follow a similar structure to the example
- **Subject-Aware Formatting**: Different examples for Physics, Biology, and Math
- **Improved Explanations**: Examples demonstrate proper use of formatting (lists, bold text, etc.)
- **Educational Style**: Ensures responses maintain an educational tone appropriate for students

## How to Use One-Shot Prompting

### In the Web Interface

1. Open the Streamlit web interface
2. In the sidebar, toggle the "Use One-Shot Prompting" switch to ON
3. Select your desired subject from the dropdown menu
4. Enter your question and click "Ask"

The system will automatically select an appropriate example based on your chosen subject.

### Via API

When making API calls, include the `use_one_shot` parameter:

```python
payload = {
    "question": "Explain the concept of wave-particle duality",
    "subject": "Physics",
    "temperature": 0.2,
    "use_one_shot": True
}

response = requests.post(
    "http://localhost:8080/ask",
    json=payload,
    headers={'Content-Type': 'application/json'}
)
```

### Using the Demo Script

We've included a demo script that compares responses with and without one-shot prompting:

```bash
python demo_one_shot.py
```

This will demonstrate the difference in response quality and formatting for Physics, Biology, and Math questions.

## Current Examples

The system includes one-shot examples for:

- **Physics**: Explains Newton's second law of motion
- **Biology**: Describes the process of photosynthesis
- **Mathematics**: Explains integration in calculus

These examples demonstrate proper use of headings, bullet points, mathematical formatting, and educational style.
