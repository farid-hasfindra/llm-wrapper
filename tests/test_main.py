from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
import pytest

client = TestClient(app)

# Mocking the Gemini Client to avoid real API calls
@pytest.fixture
def mock_gemini():
    with patch("app.api.v1.chat.GeminiClient") as MockClient:
        mock_instance = MockClient.return_value
        # Mock generate_content
        mock_instance.generate_content.return_value = "This is a mocked response."
        yield mock_instance

# Mocking the RAG Pipeline
@pytest.fixture
def mock_rag():
    with patch("app.api.v1.chat.RAGPipeline") as MockRAG:
        mock_instance = MockRAG.return_value
        # Mock run method
        mock_instance.run.return_value = {
            "answer": "This is a mocked RAG response.",
            "source_documents": [{"page_content": "Doc 1", "metadata": {"source": "test.txt"}}]
        }
        yield mock_instance

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_chat_basic(mock_gemini):
    """Test standard chat functionality (without RAG)."""
    payload = {
        "message": "Hello AI",
        "use_rag": False
    }
    response = client.post("/api/v1/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "This is a mocked response."
    assert data["message"] == "Hello AI"
    assert data["rag_enabled"] is False

def test_chat_rag(mock_rag):
    """Test RAG chat functionality."""
    payload = {
        "message": "What is in the docs?",
        "use_rag": True
    }
    # Need to patch the get_api_key dependency if auth is enabled, 
    # but for now it's auto_error=False in security.py
    response = client.post("/api/v1/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "This is a mocked RAG response."
    assert data["rag_enabled"] is True
    # Verify sources are returned
    assert len(data["sources"]) > 0
    assert data["sources"][0]["content"] == "Doc 1"

def test_admin_stats():
    """Test the admin stats endpoint."""
    response = client.get("/api/v1/admin/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
    assert "active_users" in data

def test_document_upload_validation():
    """Test document upload input validation."""
    # Test uploading a non-txt file (e.g., .png)
    files = {'file': ('test.png', b'fake image content', 'image/png')}
    response = client.post("/api/v1/documents/upload", files=files)
    
    # Should fail because we only allow .txt in the code currently
    assert response.status_code == 400
    assert "Only .txt files" in response.json()["detail"]
