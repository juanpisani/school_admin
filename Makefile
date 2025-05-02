# Project name
PROJECT_NAME := school_admin

# Docker image name
IMAGE_NAME := $(PROJECT_NAME)
# Docker Compose file name
COMPOSE_FILE := local.yml

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  build         Build the Docker image"
	@echo "  up            Start the Docker Compose services"
	@echo "  down          Stop the Docker Compose services"
	@echo "  test          Run the tests inside the container"
	@echo "  migrate       Run database migrations"
	@echo "  makemigrations Create new database migrations"
	@echo "  shell         Open a shell inside the Django container"
	@echo "  rebuild       Rebuild the Docker image and restart Compose services"
	@echo "  help          Display this help message"

# Build the Docker image
build:
	@echo "Building Docker image..."
	docker compose -f $(COMPOSE_FILE) build

# Run the Docker Compose services
up: build
	@echo "Starting Docker Compose services..."
	docker compose -f $(COMPOSE_FILE) up -d

# Stop the Docker Compose services
down:
	@echo "Stopping Docker Compose services..."
	docker compose -f $(COMPOSE_FILE) down

# Run the tests inside the container
test: up
	@echo "Running tests..."
	docker compose -f $(COMPOSE_FILE) run --rm django python manage.py test core

# Run the database migrations
migrate: up
	@echo "Running database migrations..."
	docker compose -f $(COMPOSE_FILE) run --rm django python manage.py migrate

# Create new database migrations
makemigrations: up
	@echo "Creating new database migrations..."
	docker compose -f $(COMPOSE_FILE) run --rm django python manage.py makemigrations

# Open a shell inside the Django container
shell: up
	@echo "Opening a shell inside the Django container..."
	docker compose -f $(COMPOSE_FILE) exec django /bin/bash

# Rebuild the Docker image and restart Compose services
rebuild: down build up

