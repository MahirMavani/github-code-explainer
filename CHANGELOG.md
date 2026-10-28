# Changelog

All notable changes to **RepoLens AI (GitHub Code Explainer)** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-28

### Added
- Repository cloning and source-tree extraction pipeline with GitPython.
- Local inference connector for Ollama running Qwen 2.5 (`qwen2.5:0.5b` / `qwen2.5:3b`).
- Cloud serverless inference connector for Hugging Face Inference API (`Qwen/Qwen2.5-Coder-32B-Instruct`).
- Streamlit web interface with real-time file tree visualization and structured explanations.
- MIT open source license and comprehensive setup documentation.

### Fixed
- Filtered binary files, virtual environments, and lockfiles from token payload.
