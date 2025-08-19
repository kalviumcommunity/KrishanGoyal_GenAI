"""
Simple implementation file to integrate Chain of Thought prompting into the RAG pipeline.

This file can be imported into rag_pipeline.py to add Chain of Thought functionality.
"""

# Chain of Thought prompting templates for different subjects
CHAIN_OF_THOUGHT_TEMPLATES = {
    "Math": """When answering this math question, please use a step-by-step Chain of Thought approach. This means:

1. Break down the problem into clearly defined steps
2. Show all your work and intermediate calculations
3. Explain the reasoning behind each step
4. Identify the formulas or principles you're using
5. Verify your answer at the end

This step-by-step approach helps ensure accuracy and makes the solution process educational and transparent.

Question: {question}

Let me solve this step by step:""",

    "Physics": """For this physics problem, I'll use a Chain of Thought approach to show the complete solution process:

1. First, I'll identify the relevant physics principles and equations
2. Then, I'll list all given information and variables we need to find
3. Next, I'll work through each step of the solution with clear reasoning
4. I'll include all calculations, showing each mathematical step
5. Finally, I'll verify the answer and confirm the units are correct

Question: {question}

Starting with a step-by-step solution:""",

    "Chemistry": """To solve this chemistry problem thoroughly, I'll use a Chain of Thought approach:

1. First, I'll identify the key chemical concepts involved
2. Then, I'll outline the relevant equations or principles
3. Next, I'll work systematically through each step of the solution
4. I'll explain my reasoning at each step
5. Finally, I'll verify the answer makes scientific sense

Question: {question}

Working through this step by step:""",

    "Biology": """For this biology question, I'll provide a Chain of Thought explanation:

1. First, I'll identify the key biological concepts involved
2. Then, I'll break down the process or mechanism into its component parts
3. Next, I'll explain each component in sequence with clear reasoning
4. I'll connect the steps to show how they form a complete process
5. Finally, I'll summarize the full explanation

Question: {question}

Let me explain this biological concept step by step:""",

    # Default template for other subjects
    "default": """To answer this question thoroughly, I'll use a Chain of Thought approach:

1. First, I'll break down the key components of the question
2. Then, I'll identify the relevant principles or concepts
3. Next, I'll work through my reasoning step by step
4. I'll make any intermediate conclusions explicit
5. Finally, I'll arrive at a complete answer

Question: {question}

Working through this step by step:"""
}
