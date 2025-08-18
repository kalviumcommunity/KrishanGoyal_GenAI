from .embedding_store import similarity_search
from .llm import generate_answer
from .config import settings
from typing import List, Optional, Dict

# One-shot examples for different subjects
ONE_SHOT_EXAMPLES = {
    "Physics": {
        "question": "What is Newton's second law of motion?",
        "answer": """# Newton's Second Law of Motion

Newton's second law of motion is a fundamental principle in classical mechanics that describes the relationship between force, mass, and acceleration.

## Key Points:
* **Mathematical Form**: F = ma
* **Definition**: The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.
* **Vector Nature**: Both force and acceleration are vectors with the same direction.

## Implications:
1. Doubling the force doubles the acceleration if mass remains constant
2. Doubling the mass halves the acceleration if force remains constant
3. An object with zero net force has zero acceleration (continues in its state of rest or uniform motion)

## Applications:
* Determining the force needed to accelerate vehicles
* Calculating rocket thrust requirements
* Analyzing collisions and impacts

## Summary:
Newton's second law (F = ma) is central to classical mechanics, allowing us to predict how objects move when forces act upon them. It quantifies the relationship between force, mass, and acceleration, showing that heavier objects require more force to achieve the same acceleration as lighter objects."""
    },
    "Biology": {
        "question": "Explain the process of photosynthesis.",
        "answer": """# Photosynthesis

Photosynthesis is the process by which green plants, algae, and certain bacteria convert light energy into chemical energy.

## Basic Equation:
6CO₂ + 6H₂O + Light Energy → C₆H₁₂O₆ + 6O₂

## Key Components:
* **Chlorophyll**: The green pigment that captures light energy
* **Chloroplasts**: Cell organelles where photosynthesis occurs
* **Thylakoids**: Membrane structures inside chloroplasts that contain chlorophyll

## Two Main Stages:
1. **Light-dependent reactions**:
   * Occur in thylakoid membranes
   * Convert light energy to chemical energy (ATP and NADPH)
   * Split water molecules, releasing oxygen
   
2. **Calvin Cycle (Light-independent reactions)**:
   * Takes place in the stroma
   * Uses ATP and NADPH from the first stage
   * Fixes carbon dioxide into glucose
   * Regenerates the initial CO₂ acceptor

## Importance:
* Produces oxygen essential for aerobic organisms
* Creates glucose as an energy source for plants
* Forms the foundation of most food chains
* Helps regulate atmospheric carbon dioxide levels

## Summary:
Photosynthesis is the fundamental process that converts solar energy into chemical energy, producing oxygen and carbohydrates that sustain nearly all life on Earth."""
    },
    "Math": {
        "question": "What is integration in calculus?",
        "answer": """# Integration in Calculus

Integration is a fundamental concept in calculus that represents the process of finding antiderivatives and calculating areas under curves.

## Key Definitions:
* **Indefinite Integral**: The set of all antiderivatives of a function
  * Notation: ∫f(x)dx = F(x) + C, where F'(x) = f(x)
  * C is the constant of integration
  
* **Definite Integral**: The signed area between a function and the x-axis over an interval
  * Notation: ∫[a,b]f(x)dx = F(b) - F(a), where F'(x) = f(x)

## Basic Properties:
1. ∫[a,b]k·f(x)dx = k·∫[a,b]f(x)dx (for constant k)
2. ∫[a,b][f(x) + g(x)]dx = ∫[a,b]f(x)dx + ∫[a,b]g(x)dx
3. ∫[a,b]f(x)dx = -∫[b,a]f(x)dx
4. ∫[a,b]f(x)dx + ∫[b,c]f(x)dx = ∫[a,c]f(x)dx

## Common Integration Techniques:
* Substitution (u-substitution)
* Integration by parts
* Partial fractions
* Trigonometric substitution

## Applications:
* Area calculation
* Volume determination
* Work and energy calculations
* Probability distributions
* Solving differential equations

## Summary:
Integration is the reverse process of differentiation, allowing us to find antiderivatives and calculate areas. It has widespread applications in physics, engineering, economics, and other fields that involve accumulation and total change."""
    }
}

SYSTEM_INSTRUCTIONS = """You are an educational assistant for Indian Class 12 NCERT subjects (Physics, Biology, Mathematics). Always base answers strictly on the provided context. If the answer is not in context, say you don't have enough textbook information.

Please provide detailed, well-structured answers following these guidelines:
1. Start with a clear introduction to the concept
2. Use bullet points or numbered lists to organize key information
3. Include relevant formulas, definitions, and examples
4. Highlight important terms or concepts in bold when appropriate
5. For mathematics, clearly show step-by-step solutions
6. For physics and biology, explain underlying principles and applications
7. Structure longer answers with appropriate subheadings
8. End with a brief summary of the main points

Make sure to format mathematical equations properly. Your goal is to provide comprehensive, exam-ready answers."""


def build_prompt(question: str, retrieved_docs: List[dict], use_one_shot: bool = False, subject: Optional[str] = None) -> str:
    # Build context from retrieved documents
    context_blocks = []
    for i, doc in enumerate(retrieved_docs, 1):
        context_blocks.append(f"[Source {i}]\n{doc['text']}")
    context = "\n\n".join(context_blocks)
    
    # Add one-shot example if requested
    one_shot_example = ""
    if use_one_shot:
        # Choose the appropriate example based on subject
        example_subject = "Math"  # Default
        if subject:
            if "physics" in subject.lower():
                example_subject = "Physics"
            elif "bio" in subject.lower():
                example_subject = "Biology"
                
        # Get example Q&A pair
        example = ONE_SHOT_EXAMPLES.get(example_subject, ONE_SHOT_EXAMPLES["Math"])
        one_shot_example = f"""### Example Question:
{example['question']}

### Example Answer:
{example['answer']}

Now answer the user's question in a similar format:
"""
    
    # Build the final prompt
    prompt = f"{SYSTEM_INSTRUCTIONS}\n\nContext:\n{context}\n\n{one_shot_example}Question: {question}\nAnswer:"
    return prompt


def answer_question(question: str, temperature: float | None = None, k: int | None = None, subject: Optional[str] = None, use_one_shot: bool = False):
    if not question:
        return {"error": "Question cannot be empty"}
    
    if temperature is None:
        temperature = settings.temperature_default
    if k is None:
        k = settings.max_retrieve
    retrieved = similarity_search(question, k=k, subject=subject)
    prompt = build_prompt(question, retrieved, use_one_shot=use_one_shot, subject=subject)
    answer = generate_answer(prompt, temperature=temperature)
    # Not returning sources in the response
    return {"answer": answer, "used_k": k, "temperature": temperature, "used_one_shot": use_one_shot}
