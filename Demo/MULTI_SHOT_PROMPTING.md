# Multi-Shot Prompting Guide

## What is Multi-Shot Prompting?

Multi-shot prompting is a technique where we provide the language model with multiple examples of the desired input-output format before asking it to respond to a new question. By showing multiple examples, the model can better understand patterns, formatting expectations, and the desired style for different types of questions within a subject area.

## Benefits of Multi-Shot Prompting

- **Enhanced Pattern Recognition**: Multiple examples help the model identify common patterns and structures
- **Greater Style Consistency**: More examples lead to more consistent response formatting
- **Subject-Specific Templates**: Multiple subject-specific examples guide specialized responses
- **Improved Coverage**: Different examples can demonstrate different aspects of good responses
- **Better Handling of Edge Cases**: Multiple examples can cover simple and complex question types

## How Multi-Shot Compares to One-Shot

| Aspect                | One-Shot          | Multi-Shot                       |
| --------------------- | ----------------- | -------------------------------- |
| **Examples Provided** | Single example    | Multiple examples (typically 3+) |
| **Pattern Learning**  | Limited           | More comprehensive               |
| **Response Style**    | Basic consistency | Greater stylistic adherence      |
| **Edge Cases**        | Not addressed     | Better coverage                  |
| **Token Usage**       | Lower             | Higher                           |
| **Response Time**     | Faster            | Slightly slower                  |

## How to Use Multi-Shot Prompting

### In the Web Interface

1. Open the Streamlit web interface
2. In the sidebar under "Prompt Engineering", select "Multi-Shot" from the radio buttons
3. Select your desired subject from the dropdown menu
4. Enter your question and click "Ask"

The system will automatically select appropriate examples based on your chosen subject.

### Via API

When making API calls, include the `use_multi_shot` parameter:

```python
payload = {
    "question": "Explain the concept of wave-particle duality",
    "subject": "Physics",
    "temperature": 0.2,
    "use_multi_shot": True
}

response = requests.post(
    "http://localhost:8080/ask",
    json=payload,
    headers={'Content-Type': 'application/json'}
)
```

### Using the Demo Script

We've included a demo script that compares responses with no examples, one-shot, and multi-shot prompting:

```bash
python demo_multi_shot.py
```

This will demonstrate the difference in response quality and formatting across all three prompting strategies.

## Current Examples

The system includes multi-shot examples for:

### Physics

1. Newton's second law of motion
2. Coulomb's Law and its significance
3. The principle of conservation of energy

### Biology

1. The process of photosynthesis
2. The process of mitosis
3. The structure and function of DNA

### Mathematics

1. Integration in calculus
2. Derivatives in calculus
3. Matrices and their operations

Each subject includes three carefully crafted examples that demonstrate proper use of headings, bullet points, mathematical formatting, and educational style appropriate for Class 12 students.
