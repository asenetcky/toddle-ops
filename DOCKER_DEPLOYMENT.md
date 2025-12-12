# ToddleOps Docker Deployment Guide

This guide explains how to deploy the ToddleOps application using Docker.

## Prerequisites

- Docker installed (version 20.10 or higher)
- Docker Compose installed (version 2.0 or higher)
- Access to required services:
  - Google API key for Gemini models
  - Supabase database (or alternative PostgreSQL database)
  - Ollama running locally or accessible (optional, for local LLM)

## Quick Start

### 1. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your actual values:
- `GOOGLE_API_KEY`: Your Google API key for Gemini
- `SUPABASE_PASSWORD`: Your Supabase database password
- `SUPABASE_USER`: Your Supabase database user
- `SUPABASE_CONN_STRING`: Full PostgreSQL connection string
- `OLLAMA_API_BASE`: Ollama API endpoint (if using local LLM)

### 2. Build and Run with Docker Compose

```bash
# Build and start the application
docker compose up -d

# View logs
docker compose logs -f

# Stop the application
docker compose down
```

The application will be available at: `http://localhost:8000`

### 3. Build and Run with Docker (without Compose)

```bash
# Build the Docker image
docker build -t toddle-ops .

# Run the container
docker run -d \
  --name toddle-ops \
  -p 8000:8000 \
  --env-file .env \
  toddle-ops

# View logs
docker logs -f toddle-ops

# Stop the container
docker stop toddle-ops
docker rm toddle-ops
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google API key for Gemini models | Yes |
| `SUPABASE_PASSWORD` | Supabase database password | Yes |
| `SUPABASE_USER` | Supabase database user | Yes |
| `SUPABASE_CONN_STRING` | PostgreSQL connection string | Yes |
| `OLLAMA_API_BASE` | Ollama API endpoint | No (if using Gemini only) |
| `ADK_WEB_HOST` | Host to bind the web server | No (default: 0.0.0.0) |
| `ADK_WEB_PORT` | Port for the web server | No (default: 8000) |

### Ollama Integration

If you want to use Ollama models:

1. **Run Ollama locally:**
   ```bash
   # On host machine
   ollama serve
   ```
   
2. **Update OLLAMA_API_BASE in .env:**
   ```bash
   # For Docker on Linux
   OLLAMA_API_BASE="http://host.docker.internal:11434"
   
   # Or use Docker networking
   OLLAMA_API_BASE="http://172.17.0.1:11434"
   ```

3. **Or run Ollama in Docker:**
   Add to `docker-compose.yml`:
   ```yaml
   ollama:
     image: ollama/ollama:latest
     ports:
       - "11434:11434"
     volumes:
       - ollama-data:/root/.ollama
   
   volumes:
     ollama-data:
   ```

## Development

### Local Development without Docker

```bash
# Install dependencies
uv pip install -e .

# Run with ADK web server
adk web src/toddle_ops/agents
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker compose up -d --build

# Or with Docker
docker build -t toddle-ops .
docker stop toddle-ops
docker rm toddle-ops
docker run -d --name toddle-ops -p 8000:8000 --env-file .env toddle-ops
```

## Deployment to Production

### Cloud Deployment Options

1. **Google Cloud Run:**
   ```bash
   # Build for Cloud Run
   gcloud builds submit --tag gcr.io/YOUR-PROJECT/toddle-ops
   
   # Deploy
   gcloud run deploy toddle-ops \
     --image gcr.io/YOUR-PROJECT/toddle-ops \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

2. **AWS ECS/Fargate:**
   - Push image to ECR
   - Create ECS task definition
   - Deploy service with environment variables

3. **DigitalOcean App Platform:**
   - Connect GitHub repository
   - Use Dockerfile for deployment
   - Configure environment variables in dashboard

### Environment Security

**Never commit `.env` to version control!**

For production:
- Use secrets management (AWS Secrets Manager, Google Secret Manager, etc.)
- Set environment variables through your cloud provider's dashboard
- Use encrypted environment files
- Rotate credentials regularly

## Troubleshooting

### Container won't start

Check logs:
```bash
docker compose logs toddle-ops
```

Common issues:
- Missing environment variables
- Database connection errors
- Invalid API keys

### Database Connection Issues

Verify connection string:
```bash
docker exec -it toddle-ops python -c "import os; print(os.getenv('SUPABASE_CONN_STRING'))"
```

### Port Already in Use

Change the port in `docker-compose.yml`:
```yaml
ports:
  - "9000:8000"  # Use port 9000 instead
```

## Monitoring

### Health Check

The ADK web server exposes health endpoints:
- Main UI: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

### Logs

View real-time logs:
```bash
docker compose logs -f toddle-ops
```

## Support

For issues or questions:
- Check the main [README.md](README.md)
- Review Google ADK documentation
- Open an issue on GitHub
