# LLM Wrapper Portfolio Project

A production-grade LLM Wrapper built with FastAPI, LangChain, and Google Gemini.

## Features
- **FastAPI**: High performance, easy to learn, fast to code, ready for production.
- **LangChain**: Building applications with LLMs through composability.
- **RAG (Retrieval Augmented Generation)**: Chat with your data using Gemini Embeddings and ChromaDB.
- **Structured Logging**: JSON logs for easy observability.
- **Dockerized**: Ready for deployment.

## Quick Start

### Prerequisites
- Python 3.10+
- Google API Key

### Installation

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure `.env`:
   ```bash
   cp .env.example .env
   # Edit .env and set GOOGLE_API_KEY
   ```

### Running

**Start the API:**
```bash
uvicorn app.main:app --reload
```

**Ingest Documents for RAG:**
```bash
python scripts/ingest_docs.py
```

**Docker:**
```bash
docker-compose -f infra/docker/docker-compose.yml up --build
```

## API Documentation
Once running, visit `http://localhost:8000/docs` for Swagger UI.
