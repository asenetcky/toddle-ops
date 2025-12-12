# ToddleOps Docker Quick Reference

## 🚀 Quick Start

```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your credentials

# 2. Run with Docker Compose
make docker-run

# 3. Access the app
# Open http://localhost:8000 in your browser
```

## 📋 Common Commands

```bash
# Using Makefile (recommended)
make docker-build     # Build the Docker image
make docker-run       # Start the application
make docker-stop      # Stop the application
make docker-logs      # View logs
make docker-rebuild   # Rebuild and restart
make docker-clean     # Stop and remove all containers/volumes

# Using Docker Compose directly
docker-compose up -d          # Start in background
docker-compose logs -f        # Follow logs
docker-compose down           # Stop
docker-compose up -d --build  # Rebuild and start

# Using Docker directly
docker build -t toddle-ops .
docker run -d -p 8000:8000 --env-file .env --name toddle-ops toddle-ops
docker logs -f toddle-ops
docker stop toddle-ops
```

## 🔧 Configuration

Edit `.env` file:
```bash
GOOGLE_API_KEY=your-key-here
SUPABASE_PASSWORD=your-password
SUPABASE_USER=your-user
SUPABASE_CONN_STRING=postgresql://...
OLLAMA_API_BASE=http://localhost:11434
```

## 📊 Monitoring

- **Web UI:** http://localhost:8000
- **Dev UI:** http://localhost:8000/dev-ui/
- **Logs:** `make docker-logs`

## ⚠️ Troubleshooting

**Port already in use?**
Edit `docker-compose.yml`, change port mapping:
```yaml
ports:
  - "9000:8000"  # Use different port
```

**Database connection issues?**
Check your `.env` file and verify credentials.

**Need to see what's running?**
```bash
docker ps
docker compose ps
```

## 📚 Documentation

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for full documentation.
