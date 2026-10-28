# 🔍 RepoLens AI — Local & Cloud GitHub Repository Code Explainer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000.svg)](https://ollama.com/)
[![Qwen](https://img.shields.io/badge/Model-Qwen%202.5-6366F1.svg)](https://huggingface.co/Qwen)

> **A GenAI application that accepts any public GitHub repository URL, clones and extracts its source architecture, and synthesizes clear, structured explanations using local Ollama or cloud Hugging Face Qwen 2.5 models.**

---

## 🏗️ Architecture

```
GitHub Repository
  → Repository Processing (GitPython + Code Processor)
  → Qwen AI Model (Ollama locally / Hugging Face Serverless on Cloud)
  → Streamlit Frontend
  → Structured Beginner-Friendly Explanation
```

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Backend/Processing:** Python, GitPython, FastAPI, Pydantic
- **AI Models:**
  - **Local:** Ollama + Qwen 2.5 (`qwen2.5:0.5b` or `qwen2.5:3b`)
  - **Cloud:** Hugging Face Serverless Inference API (`Qwen/Qwen2.5-Coder-32B-Instruct`)

---

## 1. Local Run (Ollama)

### Prerequisites

1. Python 3.10+
2. Git
3. Ollama (download from [ollama.com](https://ollama.com))

Install dependencies:
```bash
pip install -r requirements.txt
```

Download and run the local Qwen model:
```bash
ollama run qwen2.5:0.5b
```

### Launch the App

```bash
streamlit run frontend/app.py
```

The app will automatically detect your local Ollama instance and use it for inference.

---

## 2. Cloud Deployment (Streamlit Cloud)

When deployed to Streamlit Community Cloud:

1. The app connects to the **Hugging Face Serverless Inference API** running Qwen 2.5 on cloud GPUs (lightweight and fast, with zero heavy local CPU model loading).
2. Configure your free Hugging Face User Access Token:
   - In Streamlit Cloud: Go to **App Settings** → **Secrets** and add:
     ```toml
     HF_TOKEN = "hf_your_token_here"
     ```
   - Or enter it directly in the app's sidebar under **Cloud AI Settings**.
   - Create a free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

---

## 🧪 Example Repositories to Test

Use public repository URLs such as:
- `https://github.com/psf/requests`
- `https://github.com/pallets/click`

The application will:
1. Validate the GitHub URL.
2. Clone the repository into a temporary workspace.
3. Find relevant source-code files and filter out noise (tests, lock files, virtual environments).
4. Extract a bounded amount of source code.
5. Send the code to Qwen AI.
6. Display a clean, structured explanation and file map.

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).
