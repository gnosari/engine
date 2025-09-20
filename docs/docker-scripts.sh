#!/bin/bash

# Docker scripts for Gnosari Documentation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Build the documentation Docker image
build_docs() {
    print_status "Building Gnosari documentation Docker image..."
    docker build -t gnosari-docs .
    print_status "Build completed successfully!"
}

# Run the documentation server
run_docs() {
    print_status "Starting Gnosari documentation server..."
    docker run -d \
        --name gnosari-docs \
        -p 3000:3000 \
        --restart unless-stopped \
        gnosari-docs
    print_status "Documentation server started on http://localhost:3000"
}

# Run development server
run_dev() {
    print_status "Starting Gnosari documentation development server..."
    docker run -d \
        --name gnosari-docs-dev \
        -p 3001:3000 \
        -v "$(pwd):/app" \
        -v /app/node_modules \
        gnosari-docs-dev
    print_status "Development server started on http://localhost:3001"
}

# Stop the documentation server
stop_docs() {
    print_status "Stopping Gnosari documentation server..."
    docker stop gnosari-docs 2>/dev/null || print_warning "Container not running"
    docker rm gnosari-docs 2>/dev/null || print_warning "Container not found"
    print_status "Documentation server stopped"
}

# Stop development server
stop_dev() {
    print_status "Stopping Gnosari documentation development server..."
    docker stop gnosari-docs-dev 2>/dev/null || print_warning "Container not running"
    docker rm gnosari-docs-dev 2>/dev/null || print_warning "Container not found"
    print_status "Development server stopped"
}

# Show logs
show_logs() {
    print_status "Showing documentation server logs..."
    docker logs -f gnosari-docs
}

# Show development logs
show_dev_logs() {
    print_status "Showing development server logs..."
    docker logs -f gnosari-docs-dev
}

# Clean up Docker resources
cleanup() {
    print_status "Cleaning up Docker resources..."
    docker stop gnosari-docs gnosari-docs-dev 2>/dev/null || true
    docker rm gnosari-docs gnosari-docs-dev 2>/dev/null || true
    docker rmi gnosari-docs gnosari-docs-dev 2>/dev/null || true
    print_status "Cleanup completed"
}

# Show help
show_help() {
    echo "Gnosari Documentation Docker Scripts"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build       Build the documentation Docker image"
    echo "  run         Run the production documentation server"
    echo "  dev         Run the development server with hot reloading"
    echo "  stop        Stop the production server"
    echo "  stop-dev    Stop the development server"
    echo "  logs        Show production server logs"
    echo "  logs-dev    Show development server logs"
    echo "  cleanup     Clean up all Docker resources"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build && $0 run     # Build and run production server"
    echo "  $0 dev                  # Run development server"
    echo "  $0 logs                 # View production server logs"
}

# Main script logic
case "${1:-help}" in
    build)
        build_docs
        ;;
    run)
        run_docs
        ;;
    dev)
        run_dev
        ;;
    stop)
        stop_docs
        ;;
    stop-dev)
        stop_dev
        ;;
    logs)
        show_logs
        ;;
    logs-dev)
        show_dev_logs
        ;;
    cleanup)
        cleanup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac