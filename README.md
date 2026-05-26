# PDF RAG Chatbot with NVIDIA NIM & UV

A ultra-fast, lightweight terminal-based Retrieval-Augmented Generation (RAG) chatbot that leverages cloud-hosted NVIDIA Inference Microservices (NIM) via LangChain and uses `uv` for blistering fast Python dependency management.

## 🛠️ Setup Instructions

Follow these step-by-step instructions to set up your environment, install dependencies, and run the chatbot.

---

### Install `uv`

`uv` is an extremely fast Python package installer and resolver written in Rust. It replaces traditional `pip` workflows.

* **On macOS/Linux:**
```bash
  curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

* **On Windows**
```bash
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

* **Or, from pip**
```bash
  pip install uv
```

### Generate an NVIDIA API Key

This project requires an API key to communicate with cloud-hosted NVIDIA Inference Microservices (NIM) for text embeddings and language models.

1. Navigate to the official [NVIDIA API Catalog](https://build.nvidia.com/).
2. Click **Sign In** in the top right corner. Create a free NVIDIA Developer account or log in with your existing credentials.
3. Browse the catalog or search for your preferred model (e.g., `meta/llama-3.3-70b-instruct`).
4. Click on the model card, then select the **Get API Key** button.
5. Click **Generate Key** on the prompt. 
6. **Important:** Copy the generated key immediately and save it in a secure location. It will begin with the prefix `nvapi-`. For security reasons, NVIDIA will not show this key to you again.

### Create a `.env` File

Secure your secrets by keeping them out of your source code.

1. In the root directory of this project, create a new file named `.env`.
2. Open the file in your preferred text editor and add your API key exactly like this:

```bash
  NVIDIA_API_KEY=<YOUR_NVIDIA_API_KEY_HERE>
```

### Sync `uv` Dependencies

With `uv`, you don't need to manually create virtual environment folders. The `sync` command reads the project configuration, automatically builds a local `.venv` folder, and installs all required packages deterministically:

```bash
  uv sync
```

## 🏃 Execution Guide

Execute `main.py` using `uv run`:

* **Windows (PowerShell / CMD) & macOS / Linux:**
```bash
  uv run main.py
```
