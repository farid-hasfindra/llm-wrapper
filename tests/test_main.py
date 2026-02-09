from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
from app.main import app
import pytest

client = TestClient(app)

# Mocking the Gemini Client instance directly
@pytest.fixture
def mock_gemini():
    # We patch 'app.api.v1.chat.gemini_client' because that's the instance used in chat endpoint
    with patch("app.api.v1.chat.gemini_client") as MockClientInstance:
        # Mock generate_response (it's async, so use AsyncMock or ensure return_value is awaitable)
        MockClientInstance.generate_response = AsyncMock(return_value="This is a mocked response.")
        yield MockClientInstance

# Mocking the RAG Pipeline function
@pytest.fixture
def mock_rag():
    # We patch 'app.api.v1.chat.generate_rag_response' function
    with patch("app.api.v1.chat.generate_rag_response", new_callable=AsyncMock) as mock_function:
        mock_function.return_value = "This is a mocked RAG response."
        yield mock_function

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    # Updated expectation based on actual implementation in app/api/v1/health.py
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

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

def test_chat_rag(mock_rag):
    """Test RAG chat functionality."""
    payload = {
        "message": "What is in the docs?",
        "use_rag": True
    }
    response = client.post("/api/v1/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "This is a mocked RAG response."

def test_admin_stats():
    """Test the admin stats endpoint."""
    # Ensure correct path based on app/api/v1/admin.py and router prefix in main.py
    response = client.get("/api/v1/admin/stats")
    
    # If using TestClient, headers might need adjustment if dependency injection enforces it.
    # But in security.py, auto_error=False, so it might pass or return None user.
    # In admin.py, it depends on get_api_key.
    assert response.status_code == 200
    data = response.json()
    assert "requests_processed" in data
    assert "average_latency_ms" in data

def test_document_upload_validation():
    """Test document upload input validation."""
    # Test uploading a non-txt file (e.g., .png)
    files = {'file': ('test.png', b'fake image content', 'image/png')}
    response = client.post("/api/v1/documents/upload", files=files)
    
    # Should fail because we only allow .txt in the code currently
    assert response.status_code == 400
    assert "Only .txt files" in response.json()["detail"]
