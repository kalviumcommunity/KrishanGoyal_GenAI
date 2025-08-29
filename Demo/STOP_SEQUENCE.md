# Stop Sequence in LLM API Calls

A stop sequence is a special string or token that tells a language model when to stop generating output. This is useful for controlling the length and structure of responses, especially in educational or conversational applications.

## Why Use a Stop Sequence?
- **Prevents Overgeneration:** Stops the model from producing unnecessary or irrelevant text after the answer.
- **Ensures Clean Output:** Useful for APIs or UIs that need to parse or display only the main answer.
- **Customizable:** You can define any string as a stop sequence, such as `\n---END---` or a special token.

## How It Works
When you send a prompt to the LLM, you can include a `stop_sequence` parameter. The model will stop generating text as soon as it encounters this sequence in its output.

### Example
Suppose you ask:

> What is the quadratic formula?

With a stop sequence of `\n---END---`, the model might return:

```
The quadratic formula is:

x = [-b ± sqrt(b²-4ac)] / (2a)

---END---
```

The output will stop at `---END---`, and you can easily remove this marker in your application.

## Demo Script
See `demo_stop_sequence.py` for a hands-on demonstration. The script compares responses with and without a stop sequence, showing the effect on output and token usage.

## When to Use
- When you want to limit the answer to a single response
- When integrating with chatbots or APIs that require clean output
- When you want to prevent the model from hallucinating or rambling

## Integration
To use a stop sequence in your API call, simply add a `stop_sequence` parameter to your request payload:

```python
payload = {
    "question": "What is the quadratic formula?",
    "subject": "Math",
    "stop_sequence": "\n---END---"
}
```

## Best Practices
- Choose a stop sequence that is unlikely to appear in normal answers
- Test with your data to ensure the stop sequence works as intended
- Remove the stop sequence from the final output before displaying to users

---

Stop sequences are a simple but powerful tool for controlling LLM output in educational and other applications.
