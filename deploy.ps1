
# Deploy Script for LLM Wrapper Portfolio to Google Cloud Run
write-host "========================================================" -ForegroundColor Cyan
write-host "   LLM Wrapper Portfolio - Cloud Run Deployer 🚀"
write-host "========================================================" -ForegroundColor Cyan

# 1. Configuration
$projectID = Read-Host "Enter your Google Cloud Project ID"
if (-not $projectID) {
    write-host "Project ID is required!" -ForegroundColor Red
    exit 1
}

$region = Read-Host "Enter Region (default: us-central1)"
if (-not $region) { $region = "us-central1" }

$apiKey = Read-Host "Enter your Google Gemini API KEY (for backend env var)"

write-host "`n[1/4] Configuring Project..." -ForegroundColor Yellow
cmd /c "gcloud config set project $projectID"
cmd /c "gcloud config set run/region $region"
cmd /c "gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com"

# 2. Backend Deployment
write-host "`n[2/4] Building & Deploying Backend..." -ForegroundColor Yellow
$backendImage = "gcr.io/$projectID/llm-backend"

# Build using Cloud Build
cmd /c "gcloud builds submit --tag $backendImage ."

# Deploy Service
if ($apiKey) {
    cmd /c "gcloud run deploy llm-backend --image $backendImage --platform managed --allow-unauthenticated --set-env-vars GOOGLE_API_KEY=$apiKey"
} else {
    # If key not provided, warn user they might need to set it later
    write-host "Warning: No API Key provided. Backend may fail until key is set." -ForegroundColor Magenta
    cmd /c "gcloud run deploy llm-backend --image $backendImage --platform managed --allow-unauthenticated"
}

# Get Backend URL
$backendUrl = cmd /c "gcloud run services describe llm-backend --format='value(status.url)'"
write-host "Backend deployed at: $backendUrl" -ForegroundColor Green

# 3. Summary
write-host "`n========================================================" -ForegroundColor Cyan
write-host "   DEPLOYMENT COMPLETE! 🎉"
write-host "========================================================" -ForegroundColor Cyan
write-host "Backend API : $backendUrl" -ForegroundColor Green
write-host "Docs (Swagger): $backendUrl/docs" -ForegroundColor Green
write-host "========================================================" -ForegroundColor Cyan
write-host "Press Enter to exit..."
Read-Host
