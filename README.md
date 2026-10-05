# Local GitHub Repository Code Explainer

A student-friendly GenAI mini project that accepts a public GitHub repository URL, clones the repository locally, extracts relevant source-code files, sends the code to a locally running LLM through Ollama, and displays a simple-language explanation in a Streamlit frontend.

## Architecture

GitHub Repository
→ Repository Processing
→ Local LLM (Ollama + Qwen)
→ FastAPI Backend
→ Streamlit Frontend
→ Explanation

## Technology Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- GitPython
- Streamlit
- Ollama
- Qwen 2.5 3B

## Requirements

Install:

1. Python 3.10+
2. Git
3. Ollama

Then install the Python dependencies:

```bash
pip install -r requirements.txt
```

Download the local model:

```bash
ollama pull qwen2.5:3b
```

Test the model:

```bash
ollama run qwen2.5:3b
```

## Run the project

Open a terminal in the project root.

### Terminal 1 - FastAPI

```bash
uvicorn backend.main:app --reload
```

The backend will run at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### Terminal 2 - Streamlit

```bash
streamlit run frontend/app.py
```

Streamlit will show a local URL, usually:

http://localhost:8501

## Example

Use a public repository URL such as:

```text
https://github.com/psf/requests
```

The application will:

1. Validate the GitHub URL.
2. Clone the repository.
3. Find relevant source-code files.
4. Ignore common generated/binary directories.
5. Extract a bounded amount of source code.
6. Send the code to Qwen through Ollama.
7. Generate a beginner-friendly explanation.
8. Display the explanation in Streamlit.

## Important limitation

This version is designed for public GitHub repositories. Private repositories require authentication and are intentionally not handled by the basic version.

Large repositories are automatically limited so that the local LLM is not overloaded with too much code.

## Viva explanation

If the faculty asks "How does your project work?", explain:

"The user enters a public GitHub repository URL in the Streamlit frontend. The frontend sends the URL to a FastAPI backend. The backend clones the repository using GitPython and identifies relevant source-code files. The code is then combined into a controlled context and sent to a locally running Qwen model through Ollama. The model generates a simple explanation of the project, which the FastAPI backend returns to Streamlit. Finally, Streamlit displays the generated explanation to the user."

## Why local LLM?

"The project uses a local LLM so the code is processed on the user's machine rather than being sent to a cloud AI API. It also demonstrates how a GenAI application can integrate a locally running open-source model."
