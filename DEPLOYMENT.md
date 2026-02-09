# Deployment Guide: AWS EC2 (Free Tier)

This guide explains how to deploy the LLM Wrapper Portfolio to an AWS EC2 instance using Docker. This approach fits within the **AWS Basic Free Tier** (12 months for new accounts).

## Prerequisites
- AWS Account.
- GitHub Account (repo pushed).
- DockerHub Account (for storing the image).

---

## Step 1: Push Code to GitHub
Ensure your code is pushed to GitHub. This will trigger the CI/CD pipeline we created (`.github/workflows/cd.yml`).
> **Note**: You need to configure GitHub Secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`) in your repo settings for the auto-build to work.

Alternatively, you can build manually on the server (simpler for first time).

## Step 2: Launch EC2 Instance
1. **Login** to AWS Console -> **EC2** service.
2. Click **Launch Instance**.
3. **Name**: `LLM-Wrapper-Server`.
4. **OS Image**: Ubuntu Server 22.04 LTS (HVM).
5. **Instance Type**: `t2.micro` or `t3.micro` (Look for "Free tier eligible" label).
6. **Key Pair**: Create new login key pair (download the `.pem` file).
7. **Network settings**:
   - Allow SSH traffic from Anywhere (0.0.0.0/0) or My IP.
   - **Check** "Allow HTTP traffic from the internet".
   - **Check** "Allow HTTPS traffic from the internet".
8. Launch Instance.

## Step 3: Configure Security Group (Firewall)
1. Go to your Instance -> **Security** tab -> Click the **Security Group**.
2. **Edit inbound rules**.
3. Add Rule:
   - **Type**: Custom TCP
   - **Port range**: `8000` (FastAPI default) or `80` (if mapping port).
   - **Source**: Anywhere-IPv4 (`0.0.0.0/0`).
4. Save rules.

## Step 4: Connect to Server
Use your terminal (or Putty):
```bash
# Set permission for key
chmod 400 your-key.pem

# SSH into server (replace 1.2.3.4 with your EC2 Public IP)
ssh -i "your-key.pem" ubuntu@1.2.3.4
```

## Step 5: Install Docker on EC2
Run these commands inside the EC2 server:
```bash
# Update repo
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io docker-compose

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Allow ubuntu user to run docker (avoid sudo every time)
sudo usermod -aG docker $USER
```
*Logout and login again for permission to take effect.*

## Step 6: Deploy Application
### Option A: Clone & Run (Easiest)
1. Clone your repo:
   ```bash
   git clone https://github.com/your-username/llm-wrapper.git
   cd llm-wrapper
   ```
2. Create `.env` file:
   ```bash
   nano .env
   # Paste your environment variables (GOOGLE_API_KEY, etc) then Ctrl+X, Y, Enter.
   ```
3. Run with Docker Compose:
   ```bash
   docker-compose -f infra/docker/docker-compose.yml up -d --build
   ```

### Option B: Run from DockerHub (If CD is working)
```bash
docker run -d \
  --name llm-app \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e GOOGLE_API_KEY="your_actual_api_key_here" \
  yourusername/llm-wrapper:latest
```

## Step 7: Access Your API
Open your browser:
`http://<EC2-PUBLIC-IP>:8000/docs`

✅ Done! Your API is live on the internet.

## Costs
- **EC2**: Free for 750h/month (1 instance running 24/7 OK).
- **Data Transfer**: Small amount free, pay attention if uploading huge files.
- **Storage (EBS)**: 30GB free.
