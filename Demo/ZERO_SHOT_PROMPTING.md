# Zero-Shot Prompting

Zero-shot prompting is a technique where the language model is given clear instructions about how to respond without any examples of the desired format or style. Unlike one-shot or multi-shot prompting, zero-shot relies solely on the model's pre-trained knowledge and the clarity of the instructions provided.

## How it works in our system

In our educational Q&A system, zero-shot prompting:

1. Retrieves relevant context from NCERT textbooks
2. Provides the model with clear, structured instructions on how to format the answer
3. Does not include any example Q&A pairs
4. Asks the model to answer directly based on the instructions

## Implementation Details

The zero-shot system uses dedicated instructions that specify:

- How to structure educational content
- What formatting to use (headings, bullet points, etc.)
- What components to include (definitions, examples, applications)
- How to maintain an educational tone appropriate for Class 12 students

## Benefits of Zero-Shot Prompting

- **Flexibility**: Not tied to specific examples that might bias the model's responses
- **Efficiency**: Reduces prompt size by eliminating examples
- **Clarity**: Forces clear instructions that explicitly state expectations
- **Adaptability**: Can work across diverse topics without domain-specific examples

## Limitations

- May result in less consistent formatting across responses
- Relies heavily on the quality and clarity of instructions
- Requires the model to understand abstract guidance without concrete examples
- May be less effective for complex or specialized response formats

## When to Use Zero-Shot Prompting

Zero-shot prompting is ideal when:

- You have limited space in your prompt and can't include examples
- Your instructions are clear and specific enough to guide the model
- You want more diverse and natural responses not influenced by specific examples
- The response format is straightforward or commonly understood

## Code Example

```python
def build_prompt(question: str, retrieved_docs: List[dict], use_zero_shot: bool = True):
    # Build context from retrieved documents
    context_blocks = []
    for i, doc in enumerate(retrieved_docs, 1):
        context_blocks.append(f"[Source {i}]\n{doc['text']}")
    context = "\n\n".join(context_blocks)

    # Use zero-shot instructions
    instructions = ZERO_SHOT_INSTRUCTIONS

    # Build the final prompt without examples
    prompt = f"{instructions}\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    return prompt
```

## Comparison with Other Prompting Techniques

| Technique  | Examples Used     | Instruction Focus           | Use Case                                        |
| ---------- | ----------------- | --------------------------- | ----------------------------------------------- |
| Zero-Shot  | None              | Clear structure guidance    | General questions, flexible formatting          |
| One-Shot   | Single example    | Example + guidance          | Format consistency important                    |
| Multi-Shot | Multiple examples | Examples + minimal guidance | Complex formats, nuanced patterns               |
| Dynamic    | Context-specific  | Tailored to question type   | Different question types need different formats |

## Demo Usage

To see zero-shot prompting in action:

```bash
# Run the zero-shot demo
python demo_zero_shot.py
```

Or use the batch file:

```bash
demo_zero_shot.bat
```
