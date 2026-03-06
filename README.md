# AI Engineer Portfolio: LLM Wrapper API 🚀

A production-grade, headless REST API demonstrating advanced AI Engineering patterns. It seamlessly orchestrates ultra-fast text generation via **Groq** and Retrieval-Augmented Generation (RAG) using **Google Gemini Embeddings** and **ChromaDB**.

Designed specifically as a robust backend for modern Frontend/Fullstack AI applications.

---

## 🛠️ Tech Stack
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python Async API)
- **AI Orchestration**: [LangChain](https://python.langchain.com/)
- **Inference Engine (Chat)**: [Groq Cloud](https://console.groq.com/) (`llama-3.3-70b-versatile`)
- **Embeddings Engine (RAG)**: [Google Gemini](https://ai.google.dev/) (`models/gemini-embedding-001`)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/) (Local embedded)

---

## 🚀 Getting Started (Local Development)

### 1. Prerequisites
- Python 3.10+
- A valid **Groq API Key** (Create one at [console.groq.com](https://console.groq.com/keys))
- A valid **Google Gemini API Key** (Create one at [aistudio.google.com](https://aistudio.google.com/app/apikey))

### 2. Installation & Setup
Clone the repository and install dependencies:
```bash
# Create virtual environment (Optional but recommended)
python -m venv venv
# Activate it (Windows)
.\venv\Scripts\Activate.ps1
# Activate it (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Configure your environment variables:
```bash
# Copy example env file
cp .env.example .env
```
Open `.env` and fill in your API keys:
```env
GOOGLE_API_KEY=your_google_germini_api_key
GROQ_API_KEY=your_groq_api_key
```

### 3. Running the Server
Start the FastAPI server with hot-reload enabled:
```bash
uvicorn app.main:app --reload
```
The API is now running at `http://127.0.0.1:8000`.

---

## 📚 API Reference for Frontend Developers

Once the server is running, the interactive Swagger documentation is available at:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Below are the core endpoints you will need to build a UI.

### 1. Chat Completion Endpoint
Send a message to the AI. You can toggle RAG (Knowledge Base search) on or off.

**POST** `/api/v1/chat`

**Request Body (JSON):**
```json
{
  "message": "What is the capital of France?",
  "use_rag": false,
  "conversation_id": null
}
```
*Note: `use_rag: true` forces the API to search uploaded `.txt` files for context before answering.*

**Success Response (200 OK):**
```json
{
  "response": "The capital of France is Paris.",
  "rag_enabled": false,
  "sources": [],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 8,
    "total_tokens": 23,
    "estimated_cost": 0.000002
  }
}
```

### 2. Upload Document (RAG Context)
Upload a `.txt` file to be embedded and added to the AI's knowledge base. The embedding process happens in the background.

**POST** `/api/v1/documents/upload`

**Request (FormData):**
- Key: `file`
- Value: `[Your File.txt]`

### 3. Manage Documents
**DELETE** `/api/v1/documents/{filename}`
Deletes a specific document from the storage and triggers a re-ingestion of remaining files into the Vector DB.

**POST** `/api/v1/documents/reset`
Wipes the entire Vector DB and deletes all stored files. Perfect for a "Start Fresh" button in your UI.

## 🐳 Docker Deployment
If you want to run the API via Docker:
```bash
# Build and run using Docker Compose
docker-compose -f infra/docker/docker-compose.yml up --build
```

For Cloud Run deployment, utilize the included `deploy.ps1` script (Windows only).
