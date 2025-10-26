# Use a lightweight Python base image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first (for layer caching)
COPY requirements.txt .

# Install system dependencies (for pandas, numpy, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy all app files (including model.pkl and app.py)
COPY . .

# Expose Streamlit’s default port
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_PORT=8501
ENV PYTHONUNBUFFERED=1

# (Optional) Load environment variables from .env
# This is optional; Streamlit Cloud handles secrets separately
# COPY .env . 

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
