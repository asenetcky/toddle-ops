#!/bin/bash

# ToddleOps Docker Deployment Script
# This script helps you quickly deploy the ToddleOps application

set -e

echo "🚀 ToddleOps Docker Deployment"
echo "=============================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo ""
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "✅ .env file created!"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env with your actual credentials before continuing."
    echo ""
    read -p "Press Enter after you've updated the .env file, or Ctrl+C to exit..."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo ""
echo "🔨 Building Docker image..."
docker compose build

echo ""
echo "✅ Build complete!"
echo ""
echo "🚀 Starting ToddleOps..."
docker compose up -d

echo ""
echo "⏳ Waiting for application to start..."
sleep 5

# Check if container is running
if docker compose ps | grep -q "Up"; then
    echo ""
    echo "✅ ToddleOps is running!"
    echo ""
    echo "🌐 Access the application at:"
    echo "   http://localhost:8000"
    echo ""
    echo "📊 View logs with:"
    echo "   docker compose logs -f"
    echo "   or: make docker-logs"
    echo ""
    echo "🛑 Stop the application with:"
    echo "   docker compose down"
    echo "   or: make docker-stop"
    echo ""
else
    echo ""
    echo "❌ Something went wrong. Check the logs:"
    echo "   docker compose logs"
    exit 1
fi
