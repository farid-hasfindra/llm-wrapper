
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend app code
COPY . .

# Expose port (Cloud Run sets PORT env var)
ENV PORT=8080

# Command to run the app
CMD sh -c "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"
