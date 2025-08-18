# Dynamic Prompting Guide

## What is Dynamic Prompting?

Dynamic prompting is an advanced technique that automatically adapts the prompt structure based on the type of question asked. Instead of using fixed examples, the system analyzes the user's question and applies a specialized template tailored to the specific question type, ensuring the response has the most appropriate structure and content organization.

## Benefits of Dynamic Prompting

- **Question-Specific Formatting**: Tailors response structure to match what's being asked
- **Improved Organization**: Ensures content is presented in the most logical way for each question type
- **Consistent Response Quality**: Maintains high-quality formatting regardless of question complexity
- **Efficient Processing**: No need to include multiple examples in the prompt
- **Adaptable Structure**: Different types of questions get different response structures

## Question Types Detected

The dynamic prompting system can identify five distinct question types and adapt responses accordingly:

### 1. Definition Questions

- **Pattern**: What is...?, Define..., Explain the concept of...
- **Response Format**: Clear definition with key properties, related concepts, and examples
- **Example**: "What is Newton's Third Law of Motion?"

### 2. Comparison Questions

- **Pattern**: Compare..., Difference between..., Contrast...
- **Response Format**: Point-by-point comparison with similarities and differences highlighted
- **Example**: "Compare mitosis and meiosis."

### 3. Process Questions

- **Pattern**: Process of..., Steps in..., How does..., Mechanism of...
- **Response Format**: Sequential steps with clear indication of inputs, intermediate stages, and outputs
- **Example**: "Explain the process of photosynthesis."

### 4. Problem-Solving Questions

- **Pattern**: Solve..., Calculate..., Find..., Determine...
- **Response Format**: Step-by-step solution with formulas, substitutions, and clear explanation of each step
- **Example**: "Solve the definite integral of x² from 0 to 2."

### 5. Application Questions

- **Pattern**: Application of..., Used for..., Importance of..., Practical use...
- **Response Format**: Categorized applications with explanations of how the concept applies in different contexts
- **Example**: "What are the applications of logarithms in real life?"

## How to Use Dynamic Prompting

### In the Web Interface

1. Open the Streamlit web interface
2. In the sidebar under "Prompt Engineering", select "Dynamic" from the radio buttons
3. Enter your question and click "Ask"

The system will automatically detect the question type and format the response accordingly.

### Via API

When making API calls, include the `use_dynamic` parameter:

```python
payload = {
    "question": "Compare photosynthesis and cellular respiration.",
    "subject": "Biology",
    "temperature": 0.2,
    "use_dynamic": True
}

response = requests.post(
    "http://localhost:8080/ask",
    json=payload,
    headers={'Content-Type': 'application/json'}
)
```

### Using the Demo Script

We've included a demo script that shows dynamic prompting for different question types:

```bash
python demo_dynamic.py
```

This will demonstrate how the system responds differently to various question types.

## How Dynamic Prompting Compares to Other Techniques

| Aspect                  | Standard         | One-Shot         | Multi-Shot        | Dynamic                |
| ----------------------- | ---------------- | ---------------- | ----------------- | ---------------------- |
| **Template Source**     | None             | Fixed example    | Multiple examples | Question analysis      |
| **Response Structure**  | Varied           | Based on example | Based on examples | Based on question type |
| **Adaptability**        | Low              | Medium           | Medium            | High                   |
| **Pattern Recognition** | None             | Limited          | Good              | Excellent              |
| **Token Efficiency**    | High             | Medium           | Low               | High                   |
| **Best For**            | Simple questions | General guidance | Complex topics    | Varied question types  |

## Implementation Details

The dynamic prompting system uses regular expressions to analyze question patterns and match them to one of the five question types. Each question type has a custom template that guides the model on how to structure the response, what elements to include, and how to format the information.

This approach ensures that students get the most appropriate response format for their specific learning needs, whether they're asking for definitions, comparisons, processes, problem-solving, or applications.
