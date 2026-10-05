import os
import requests
import streamlit as st


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:0.5b"
)

HF_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"


def build_prompt(repository_context: str) -> str:
    return f"""
You are an expert software engineering teacher.

Your job is to understand an ENTIRE GitHub repository
and explain the project to a college student.

IMPORTANT:

- Analyze the repository as a complete project.
- Do NOT rewrite the code.
- Do NOT clean the code.
- Do NOT generate replacement code.
- Do NOT focus on one individual file.
- Do NOT reproduce large amounts of source code.
- Do NOT invent features.
- Only describe functionality that can be reasonably
  understood from the provided repository.
- Test files should NOT be treated as the main application.
- Explain everything in simple beginner-friendly language.

The repository may contain multiple programming languages,
frameworks and files.

Use the following EXACT structure.

# Project Overview

Explain:

1. What the project is.
2. What problem it solves.
3. What the application is used for.

Write approximately 3-5 sentences.

# Main Features

List the major features as bullet points.

# Project Structure

Explain the important folders and files.

Use this format:

- `filename` — explanation
- `folder/` — explanation

Focus on application files rather than tests.

# How the Application Works

Explain the complete flow of the application.

For example:

User
↓
Frontend
↓
Backend
↓
Processing
↓
Database/API
↓
Output

Use the actual architecture found in the repository.

# Technologies Used

Identify:

- Programming languages
- Frameworks
- Libraries
- Databases
- APIs
- Development tools

# Important Code Components

Explain important:

- functions
- classes
- modules
- components

Do NOT reproduce their source code.

Only explain their purpose.

# Simple Summary

Give a short explanation of the complete project
in 5-8 sentences that a beginner can understand.

Remember:

You are explaining the PROJECT.

You are NOT editing or cleaning the code.

Here is the repository:

{repository_context}
"""


def _explain_with_ollama(repository_context: str) -> str:
    prompt = build_prompt(repository_context)

    response = requests.post(
        f"{OLLAMA_URL.rstrip('/')}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_ctx": 4096,
                "num_predict": 900
            }
        },
        timeout=600
    )

    response.raise_for_status()

    data = response.json()

    explanation = data.get("response", "").strip()

    if not explanation:
        raise RuntimeError(
            "Ollama returned an empty response."
        )

    return explanation


@st.cache_resource
def load_huggingface_model():
    """
    Load Qwen 2.5 0.5B locally using Hugging Face Transformers.

    Streamlit caches the model so it is not downloaded
    every time the application reruns.
    """

    from transformers import AutoTokenizer, AutoModelForCausalLM

    tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)

    model = AutoModelForCausalLM.from_pretrained(
        HF_MODEL,
        torch_dtype="auto"
    )

    return tokenizer, model


def _explain_with_transformers(repository_context: str) -> str:
    import torch

    tokenizer, model = load_huggingface_model()

    prompt = build_prompt(repository_context)

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert software engineering teacher "
                "who explains GitHub repositories to college students."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=6000
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=900,
            temperature=0.1,
            do_sample=False
        )

    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    explanation = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    if not explanation:
        raise RuntimeError(
            "Qwen returned an empty response."
        )

    return explanation


def explain_repository(repository_context: str) -> str:
    """
    Use Ollama when available.

    If Ollama is unavailable, automatically fall back
    to the same Qwen 2.5 0.5B model through Transformers.

    This allows the same application to work both:
    - locally with Ollama
    - online on Streamlit Cloud
    """

    try:
        return _explain_with_ollama(repository_context)

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.RequestException
    ):
        return _explain_with_transformers(repository_context)