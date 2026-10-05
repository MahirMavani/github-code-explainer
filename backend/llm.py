import os
import requests


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:3b"
)


def explain_repository(repository_context: str) -> str:

    prompt = f"""
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

    try:

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

    except requests.exceptions.ConnectionError as exc:

        raise RuntimeError(
            "Cannot connect to Ollama. "
            "Make sure Ollama is running."
        ) from exc

    except requests.exceptions.Timeout as exc:

        raise RuntimeError(
            "The local LLM took too long to respond."
        ) from exc

    except requests.RequestException as exc:

        raise RuntimeError(
            f"Ollama request failed: {exc}"
        ) from exc

    data = response.json()

    explanation = data.get(
        "response",
        ""
    ).strip()

    if not explanation:

        raise RuntimeError(
            "The local LLM returned an empty response."
        )

    return explanation