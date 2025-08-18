from .embedding_store import similarity_search
from .llm import generate_answer
from .config import settings
from typing import List, Optional, Dict

# Multi-shot examples for different subjects
MULTI_SHOT_EXAMPLES = {
    "Physics": [
        {
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

## Summary:
Newton's second law (F = ma) is central to classical mechanics, allowing us to predict how objects move when forces act upon them."""
        },
        {
            "question": "Explain Coulomb's Law and its significance.",
            "answer": """# Coulomb's Law

Coulomb's Law describes the electrostatic force between charged particles.

## Mathematical Expression:
* F = k(q₁q₂)/r²

## Key Parameters:
* F = electrostatic force between charges (in newtons)
* k = Coulomb's constant (9 × 10⁹ N·m²/C²)
* q₁, q₂ = magnitudes of charges (in coulombs)
* r = distance between charges (in meters)

## Properties:
1. The force is directly proportional to the product of charges
2. The force is inversely proportional to the square of the distance
3. The force is attractive for opposite charges and repulsive for like charges
4. It follows the superposition principle for multiple charges

## Significance:
* Forms the foundation of electrostatics
* Helps calculate electric fields and potentials
* Explains atomic and molecular bonding behavior
* Similar mathematical form to Newton's Law of Gravitation"""
        },
        {
            "question": "What is the principle of conservation of energy?",
            "answer": """# Conservation of Energy

The principle of conservation of energy states that energy cannot be created or destroyed, only transformed from one form to another.

## Key Concepts:
* **Total Energy**: In an isolated system, remains constant over time
* **Energy Forms**: Includes kinetic, potential, thermal, chemical, electrical, nuclear, etc.
* **System Boundary**: Defines what is included in the energy accounting

## Mathematical Expression:
* E₁ + W + Q = E₂
  Where E₁ is initial energy, W is work done on system, Q is heat added, and E₂ is final energy

## Applications:
1. Analyzing mechanical systems (pendulums, roller coasters)
2. Studying thermal processes (heat engines, refrigerators)
3. Understanding chemical reactions and their energy changes
4. Explaining nuclear processes and radioactive decay

## Limitations:
* In relativity, mass and energy are interconvertible (E=mc²)
* In quantum mechanics, energy conservation applies within uncertainty principle constraints"""
        }
    ],
    
    "Biology": [
        {
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
* Forms the foundation of most food chains"""
        },
        {
            "question": "Describe the process of mitosis.",
            "answer": """# Mitosis

Mitosis is a type of cell division that results in two identical daughter cells from a single parent cell.

## Phases of Mitosis:
1. **Prophase**:
   * Chromosomes condense and become visible
   * Nuclear membrane begins to break down
   * Spindle fibers start to form

2. **Metaphase**:
   * Chromosomes align at the cell's equator (metaphase plate)
   * Spindle fibers attach to centromeres of chromosomes
   * Cell ensures proper chromosome alignment

3. **Anaphase**:
   * Sister chromatids separate and move toward opposite poles
   * Cell elongates as spindle fibers shorten
   * Chromosome movement is coordinated and precise

4. **Telophase**:
   * Nuclear membranes reform around separated chromosomes
   * Chromosomes decondense back into chromatin
   * Cytokinesis usually begins during this phase

## Significance:
* Enables growth and development in multicellular organisms
* Allows for tissue repair and cell replacement
* Maintains chromosome number and genetic stability
* Essential for asexual reproduction in some organisms"""
        },
        {
            "question": "What is the structure and function of DNA?",
            "answer": """# DNA: Structure and Function

DNA (Deoxyribonucleic Acid) is the genetic material that carries the hereditary information in most living organisms.

## Structure:
1. **Double Helix**: Two polynucleotide strands coiled around each other
2. **Nucleotides**: Building blocks consisting of:
   * Deoxyribose sugar
   * Phosphate group
   * Nitrogenous base (A, T, G, or C)
3. **Base Pairing**: Adenine pairs with Thymine; Guanine pairs with Cytosine
4. **Antiparallel Strands**: Strands run in opposite directions (5' to 3' and 3' to 5')

## Key Properties:
* **Complementarity**: Each strand serves as a template for the other
* **Stability**: Hydrogen bonds between base pairs and hydrophobic interactions
* **Variability**: Sequence of bases determines genetic information

## Functions:
1. **Storage of Genetic Information**: Contains genes that code for proteins
2. **Replication**: Self-duplicates during cell division
3. **Transcription**: Serves as template for RNA synthesis
4. **Mutation**: Can undergo changes that lead to genetic variation"""
        }
    ],
    
    "Math": [
        {
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

## Applications:
* Area calculation
* Volume determination
* Work and energy calculations
* Probability distributions"""
        },
        {
            "question": "Explain the concept of derivatives in calculus.",
            "answer": """# Derivatives in Calculus

A derivative measures the instantaneous rate of change of a function with respect to one of its variables.

## Formal Definition:
* f'(x) = lim[h→0] [f(x+h) - f(x)]/h

## Notation:
* f'(x), dy/dx, d/dx[f(x)], Df(x)

## Basic Rules:
1. **Power Rule**: d/dx[x^n] = nx^(n-1)
2. **Sum Rule**: d/dx[f(x) + g(x)] = f'(x) + g'(x)
3. **Product Rule**: d/dx[f(x)·g(x)] = f'(x)·g(x) + f(x)·g'(x)
4. **Quotient Rule**: d/dx[f(x)/g(x)] = [f'(x)·g(x) - f(x)·g'(x)]/[g(x)]²
5. **Chain Rule**: d/dx[f(g(x))] = f'(g(x))·g'(x)

## Geometric Interpretation:
* Slope of the tangent line to the curve at a point
* Rate of change of the function at that point

## Applications:
* Finding rates of change
* Determining local maxima and minima
* Analyzing motion (velocity, acceleration)
* Optimization problems"""
        },
        {
            "question": "What are matrices and their operations?",
            "answer": """# Matrices and Their Operations

Matrices are rectangular arrays of numbers, symbols, or expressions arranged in rows and columns.

## Basic Terminology:
* **Order/Dimension**: m × n (m rows, n columns)
* **Square Matrix**: Equal number of rows and columns
* **Identity Matrix**: Square matrix with 1s on diagonal, 0s elsewhere
* **Transpose**: A^T has rows and columns of A interchanged

## Matrix Operations:
1. **Addition and Subtraction**:
   * Must have same dimensions
   * Add/subtract corresponding elements
   * (A ± B)ᵢⱼ = Aᵢⱼ ± Bᵢⱼ

2. **Scalar Multiplication**:
   * Multiply each element by scalar
   * (kA)ᵢⱼ = k·Aᵢⱼ

3. **Matrix Multiplication**:
   * For A(m×n) × B(n×p) = C(m×p)
   * Cᵢⱼ = ∑ᵏ₌₁ⁿ Aᵢₖ·Bₖⱼ
   * Number of columns in A must equal rows in B

4. **Determinant**: (for square matrices)
   * Scalar value calculated from elements
   * Determines invertibility (non-zero)

## Applications:
* Linear transformations
* Solving systems of linear equations
* Data representation in computer graphics
* Quantum mechanics calculations"""
        }
    ]
}

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


def build_prompt(question: str, retrieved_docs: List[dict], use_one_shot: bool = False, 
              use_multi_shot: bool = False, subject: Optional[str] = None) -> str:
    # Build context from retrieved documents
    context_blocks = []
    for i, doc in enumerate(retrieved_docs, 1):
        context_blocks.append(f"[Source {i}]\n{doc['text']}")
    context = "\n\n".join(context_blocks)
    
    # Set default example text
    examples_text = ""
    
    # Determine the appropriate subject
    example_subject = "Math"  # Default
    if subject:
        if "physics" in subject.lower():
            example_subject = "Physics"
        elif "bio" in subject.lower():
            example_subject = "Biology"
    
    # Add multi-shot examples if requested (takes precedence over one-shot)
    if use_multi_shot:
        examples = MULTI_SHOT_EXAMPLES.get(example_subject, MULTI_SHOT_EXAMPLES["Math"])
        examples_blocks = []
        
        for i, example in enumerate(examples, 1):
            examples_blocks.append(f"""### Example {i} Question:
{example['question']}

### Example {i} Answer:
{example['answer']}""")
        
        examples_text = "\n\n".join(examples_blocks) + "\n\nNow answer the user's question in a similar format:"
    
    # Add one-shot example if requested and multi-shot is not being used
    elif use_one_shot:
        # Get example Q&A pair
        example = ONE_SHOT_EXAMPLES.get(example_subject, ONE_SHOT_EXAMPLES["Math"])
        examples_text = f"""### Example Question:
{example['question']}

### Example Answer:
{example['answer']}

Now answer the user's question in a similar format:"""
    
    # Build the final prompt
    prompt = f"{SYSTEM_INSTRUCTIONS}\n\nContext:\n{context}\n\n{examples_text}\n\nQuestion: {question}\nAnswer:"
    return prompt


def answer_question(question: str, temperature: float | None = None, k: int | None = None, 
                 subject: Optional[str] = None, use_one_shot: bool = False, use_multi_shot: bool = False):
    if not question:
        return {"error": "Question cannot be empty"}
    
    if temperature is None:
        temperature = settings.temperature_default
    if k is None:
        k = settings.max_retrieve
    
    # Multi-shot takes precedence over one-shot if both are enabled
    if use_multi_shot:
        use_one_shot = False
    
    retrieved = similarity_search(question, k=k, subject=subject)
    prompt = build_prompt(question, retrieved, use_one_shot=use_one_shot, use_multi_shot=use_multi_shot, subject=subject)
    answer = generate_answer(prompt, temperature=temperature)
    
    # Not returning sources in the response
    return {
        "answer": answer, 
        "used_k": k, 
        "temperature": temperature, 
        "used_one_shot": use_one_shot,
        "used_multi_shot": use_multi_shot
    }
