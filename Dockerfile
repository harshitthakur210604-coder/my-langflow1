FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port HarxitFlow (HarxitFlow) runs on
EXPOSE 7860

# Command to run the application
# We use the harxitflow command which is mapped to harxitflow.harxitflow_launcher:main
CMD ["sh", "-c", "harxitflow run --host 0.0.0.0 --port ${PORT:-7860}"]
