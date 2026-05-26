# PDF RAG Chatbot with NVIDIA NIM & UV

A ultra-fast, lightweight terminal-based Retrieval-Augmented Generation (RAG) chatbot that leverages cloud-hosted NVIDIA Inference Microservices (NIM) via LangChain and uses `uv` for blistering fast Python dependency management.

## 🛠️ Setup Instructions

Follow these step-by-step instructions to set up your environment, install dependencies, and run the chatbot.

---

### 1. Install `uv`

`uv` is an extremely fast Python package installer and resolver written in Rust. It replaces traditional `pip` workflows.

**On macOS/Linux:**
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

**On Windows**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Or, from pip**
```bash
pip install uv
```
