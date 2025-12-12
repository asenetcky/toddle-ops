# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock README.md ./

# Copy source code
COPY src ./src
COPY .env.example .env

# Install Python dependencies using uv
# Use uv pip install with the package, which will read pyproject.toml
RUN uv pip install --system -e .

# Expose port for the ADK web server
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ADK_WEB_HOST=0.0.0.0
ENV ADK_WEB_PORT=8000

# Run the application using ADK web server
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000", "src/toddle_ops/agents"]
