from .embedding_store import similarity_search
from .llm import generate_answer
from .config import settings
from typing import List, Optional

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


def build_prompt(question: str, retrieved_docs: List[dict]) -> str:
    context_blocks = []
    for i, doc in enumerate(retrieved_docs, 1):
        context_blocks.append(f"[Source {i}]\n{doc['text']}")
    context = "\n\n".join(context_blocks)
    prompt = f"{SYSTEM_INSTRUCTIONS}\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    return prompt


def answer_question(question: str, temperature: float | None = None, k: int | None = None, subject: Optional[str] = None):
    if not question:
        return {"error": "Question cannot be empty"}
    
    if temperature is None:
        temperature = settings.temperature_default
    if k is None:
        k = settings.max_retrieve
    retrieved = similarity_search(question, k=k, subject=subject)
    prompt = build_prompt(question, retrieved)
    answer = generate_answer(prompt, temperature=temperature)
    # Not returning sources in the response
    return {"answer": answer, "used_k": k, "temperature": temperature}
