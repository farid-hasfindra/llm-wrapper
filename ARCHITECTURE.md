# System Architecture 🏗️

This document outlines the internal architecture, data flow, and design patterns of the LLM Wrapper API. It is designed to serve as a comprehensive reference for Frontend, Mobile, or Fullstack developers building clients that consume this API.

## 1. High-Level Overview

This project is a high-performance **Headless REST API** built with FastAPI and LangChain. It acts as an intelligent middleware orchestrating:
1.  **Text Generation (Inference)**: Powered by **Groq** (`llama-3.3-70b-versatile` / `openai/gpt-oss-20b`) for ultra-fast completions.
2.  **Embeddings (RAG)**: Powered by **Google Gemini** (`models/gemini-embedding-001`) because Groq currently does not offer native document embedding endpoints.
3.  **Vector Database**: Powered by **ChromaDB** running embedded locally to store and retrieve document contexts.

## 2. Component Diagram

```mermaid
graph TD
    Client[Frontend / Client App] -->|REST API HTTP| API[FastAPI Server]
    API -->|Auth Check| Auth[Middleware / Security]
    
    subgraph Core Application Layer
        API -->|Route: /chat| Orchestrator[Orchestrator]
        API -->|Route: /documents| DocManager[Document Manager]
    end
    
    subgraph LLM Inference Engine (Groq)
        Orchestrator -->|Direct Question| GroqClient[Groq Client via Langchain-OpenAI]
        GroqClient -.->|API Call| GroqPlatform[Groq Cloud API]
    end
    
    subgraph RAG Pipeline (Knowledge Base)
        DocManager -->|Upload .txt| IngestionTask[Background Ingestion]
        IngestionTask -->|Chunking| LangchainSplitter[RecursiveCharacterTextSplitter]
        LangchainSplitter -->|Embed Chunks| GeminiEmbed[Google Gemini Embeddings]
        GeminiEmbed -->|Store Vectors| VectorDB[(ChromaDB)]
        
        Orchestrator -->|if use_rag=true| RetrieverChain[RetrievalQA Chain]
        RetrieverChain -->|Query| VectorDB
        VectorDB -->|Top-K Contexts| RetrieverChain
        RetrieverChain -->|Context + Prompt| GroqClient
    end
```

## 3. Directory Structure Breakdown

Understanding the `app/` directory is crucial for navigating the business logic:

*   **`app/api/`**: Contains all FastAPI router definitions. This is the entry point for HTTP requests.
    *   `v1/chat.py`: Handles the core conversational endpoint.
    *   `v1/documents.py`: Handles file uploads, deletions, and knowledge base resets.
*   **`app/core/`**: System-wide configurations.
    *   `config.py`: Pydantic settings management (loads `.env`).
    *   `security.py`: API Key validation logic.
*   **`app/llm/`**: Classes responsible for talking to external LLM providers.
    *   `groq_client.py`: Uses `ChatOpenAI` wrapper to communicate with Groq's high-speed inference engine. Extracts token usage metrics.
*   **`app/rag/`**: The entire Retrieval-Augmented Generation subsystem.
    *   `embeddings.py`: Configures the Google Gemini embedding model.
    *   `vectorstore.py`: Initializes and manages connection to local ChromaDB.
    *   `ingestion.py`: Logic for reading `.txt` files, splitting them, and saving to ChromaDB.
    *   `retriever.py`: Fetches relevant chunks based on a user query.
    *   `pipeline.py`: The LangChain LCEL (LangChain Expression Language) chain that combines the Retriever, Prompt Template, and Groq LLM.
*   **`app/schemas/`**: Pydantic models (DTOs) defining strict Input/Output structures for the API.

## 4. Feature Workflows

### 4.1. Standard Chat (No Context)
When a user sends `use_rag: false`:
1.  Request hits `ChatRouter` -> `Orchestrator`.
2.  `Orchestrator` bypasses the RAG chain.
3.  The raw user message is sent directly to `GroqClient.generate_response()`.
4.  Groq processes the request and returns the answer along with Token Usage data.

### 4.2. RAG Chat (Chat with Documents)
When a user sends `use_rag: true`:
1.  Request hits `ChatRouter` -> `Orchestrator`.
2.  `Orchestrator` delegates the prompt to `generate_rag_response()` in `pipeline.py`.
3.  **Retrieval Step**: The user's query is converted to a vector (via Gemini Embeddings) and compared against ChromaDB.
4.  **Prompt Assembly**: The top matching document chunks are retrieved and injected into a strict prompt template: *"Use the following context to answer the question..."*
5.  **Generation Step**: The assembled, massive prompt is sent to `GroqClient`.
6.  The response and the source document chunks are returned to the user.

### 4.3. Document Ingestion (Background)
To prevent API timeouts during large file uploads:
1.  File is saved to local disk `data/docs/`.
2.  FastAPI immediately returns a `200 OK` to the user indicating the upload started.
3.  FastAPI queues `ingest_docs()` as a Background Task.
4.  The task reads the file, splits it into chunks of ~1000 characters, embeds them using Gemini, and stores them in ChromaDB.

## 5. Technology Stack Decisions

*   **FastAPI**: Chosen for native `async`/`await` support necessary for non-blocking external API calls (Groq/Gemini). It also auto-generates the OpenAPI (Swagger) spec schemas.
*   **Groq (LPU)**: Chosen for the chat completions due to its extreme inference speed, providing a near-instant streaming-like feel for end-users.
*   **Google Gemini (Embeddings)**: Chosen because it offers a generous free tier for embeddings, supplementing Groq's lack of an embedding endpoint.
*   **ChromaDB**: Chosen as it can run entirely locally as an embedded SQLite-based database during development, eliminating the need for Dockerized Postgres/pgvector setups until production scale is required.
