from .embedding_store import similarity_search
from .llm import generate_answer
from .config import settings
from typing import List, Optional

SYSTEM_INSTRUCTIONS = """You are an educational assistant for Indian Class 12 NCERT subjects (Physics, Biology, Mathematics). Always base answers strictly on the provided context. If the answer is not in context, say you don't have enough textbook information. Provide concise, exam-oriented explanations unless user asks for analogies."""


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
    sources = [r["metadata"] for r in retrieved]
    return {"answer": answer, "sources": sources, "used_k": k, "temperature": temperature}
