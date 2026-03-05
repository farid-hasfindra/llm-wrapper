# Deploying to Google Cloud Run 🚀

This guide explains how to deploy the **LLM Wrapper Portfolio** (both Backend API and Frontend UI) to Google Cloud Run using the provided script.

## Prerequisites

1.  **Google Cloud SDK (gcloud CLI)** installed and authenticated.
    *   Command: `gcloud auth login`
2.  **Docker Desktop** (optional but recommended for local building, though the script uses Google Cloud Build).
3.  **Active Google Cloud Project** with billing enabled.

## Quick Start (Windows)

We have provided a PowerShell script to automate the entire process.

1.  Open PowerShell in the project root.
2.  Run the script:
    ```powershell
    .\deploy.ps1
    ```
3.  Follow the prompts:
    *   Enter your **Google Cloud Project ID** (e.g., `my-llm-project-123`).
    *   Select the region (default: `us-central1`).
    *   The script will:
        *   Build and Deploy the **Backend API**.
        *   Get the Backend URL.
        *   Build and Deploy the **Frontend UI**, injecting the Backend URL automatically.

## Manual Deployment Steps

If you prefer to run commands manually:

### 1. Set Project & Region
```bash
gcloud config set project YOUR_PROJECT_ID
gcloud config set run/region us-central1
```

### 2. Deploy Backend (API)
```bash
# Submit build to Container Registry / Artifact Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/llm-backend .

# Deploy to Cloud Run
gcloud run deploy llm-backend \
  --image gcr.io/YOUR_PROJECT_ID/llm-backend \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY="YOUR_API_KEY"
```
*Note: Replace `YOUR_API_KEY` with your actual Gemini API Key.*

### 3. Deploy Frontend (Streamlit)
After the backend is deployed, copy its URL (e.g., `https://llm-backend-xyz.a.run.app`).

```bash
# Submit build (from frontend directory context or root with specific file)
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/llm-frontend frontend/

# Deploy to Cloud Run (Pass Backend URL)
gcloud run deploy llm-frontend \
  --image gcr.io/YOUR_PROJECT_ID/llm-frontend \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars API_BASE_URL="https://llm-backend-xyz.a.run.app"
```

## Troubleshooting

-   **Backend 429 Errors**: Check the Gemini API Quota.
-   **Frontend Connection Error**: Ensure `API_BASE_URL` in the frontend service configuration matches the deployed backend URL exactly (no trailing slash issues, though the code handles basic joins).
-   **Build Failures**: Check `gcloud builds log` for details.
