# ISP-specific targets (ops frontend/backend).

# Colors
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

.PHONY: up down up-infra down-infra help \
	start-isp stop-isp restart-isp status-isp logs-isp clean-isp \
	dev dev-frontend dev-backend install check-prereqs check-docker check-deps \
	db-migrate db-migrate-create db-seed db-reset \
	test test-fast lint format \
	build-isp build-freeradius post-deploy-isp docker-isp-up docker-ps

.DEFAULT_GOAL := help

help:
	@echo "$(CYAN)╔══════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(CYAN)║  DotMac ISP Ops - Development Commands                    ║$(NC)"
	@echo "$(CYAN)╚══════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Quick Start:$(NC)"
	@echo "  make up        Start infra (Postgres/Redis) + ISP backend + run migrations"
	@echo "  make down      Stop all services"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make dev               Start ISP backend in Docker (logs follow)"
	@echo "  make dev-frontend      Start ISP Ops frontend (http://localhost:3001)"
	@echo ""
	@echo "$(GREEN)Database:$(NC)"
	@echo "  make db-migrate        Run alembic migrations"
	@echo "  make db-seed           Seed test data"
	@echo "  make db-reset          Reset and reseed database (DESTRUCTIVE)"
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@echo "  make test              Run all tests with coverage"
	@echo "  make test-fast         Run tests without coverage"
	@echo "  make lint              Run Python linting"
	@echo ""

# ===================================================================
# Quick Start - Simple up/down
# ===================================================================

up-infra:
	@echo "$(CYAN)Starting infrastructure (Postgres, Redis, MinIO)...$(NC)"
	@docker compose -f docker-compose.infra.yml up -d
	@echo "$(GREEN)✓ Infrastructure started$(NC)"

down-infra:
	@echo "$(CYAN)Stopping infrastructure...$(NC)"
	@docker compose -f docker-compose.infra.yml down
	@echo "$(GREEN)✓ Infrastructure stopped$(NC)"

up: up-infra
	@echo "$(CYAN)Starting ISP backend + services (MongoDB, GenieACS, FreeRADIUS)...$(NC)"
	@docker compose up -d isp-backend mongodb genieacs freeradius
	@echo "$(CYAN)Running database migrations...$(NC)"
	@sleep 3
	@docker compose exec isp-backend alembic upgrade head || poetry run alembic upgrade head || true
	@echo ""
	@echo "$(GREEN)✓ ISP services are running!$(NC)"
	@echo "  Backend API:  http://localhost:8000/docs"
	@echo "  GenieACS UI:  http://localhost:7577"
	@echo "  Frontend:     Run 'make dev-frontend' in another terminal"

down:
	@echo "$(CYAN)Stopping all services...$(NC)"
	@docker compose down
	@docker compose -f docker-compose.infra.yml down
	@echo "$(GREEN)✓ All services stopped$(NC)"

# ===================================================================
# Infrastructure - ISP
# ===================================================================

start-isp:
	@./scripts/infra.sh isp start

stop-isp:
	@./scripts/infra.sh isp stop

restart-isp:
	@./scripts/infra.sh isp restart

status-isp:
	@./scripts/infra.sh isp status

logs-isp:
	@./scripts/infra.sh isp logs

clean-isp:
	@./scripts/infra.sh isp clean

# ===================================================================
# Development
# ===================================================================

install: check-prereqs
	@echo "$(CYAN)Installing Python dependencies...$(NC)"
	@poetry install
	@echo "$(CYAN)Installing frontend workspace dependencies...$(NC)"
	@cd frontend && pnpm install
	@echo ""
	@echo "$(GREEN)✓ All dependencies installed successfully!$(NC)"

dev:
	@echo "$(CYAN)Starting ISP backend service inside Docker (logs follow)$(NC)"
	@echo "$(CYAN)ISP API docs: http://localhost:8000/docs$(NC)"
	@docker compose up isp-backend

dev-backend:
	@echo "$(CYAN)Starting ISP backend directly on the host (debug mode)$(NC)"
	@poetry run uvicorn dotmac.platform.main:app --host 0.0.0.0 --port 8000 --reload

dev-frontend:
	@echo "$(CYAN)Starting ISP frontend on http://localhost:3001$(NC)"
	@cd frontend && pnpm dev:isp

check-prereqs:
	@echo "$(CYAN)Checking core development dependencies...$(NC)"
	@command -v poetry >/dev/null 2>&1 || { echo "$(YELLOW)✗ Poetry not installed. Install from: https://python-poetry.org/$(NC)"; exit 1; }
	@echo "$(GREEN)✓ Poetry installed$(NC)"
	@command -v pnpm >/dev/null 2>&1 || { echo "$(YELLOW)✗ pnpm not installed. Run: npm install -g pnpm$(NC)"; exit 1; }
	@echo "$(GREEN)✓ pnpm installed$(NC)"
	@echo ""
	@echo "$(GREEN)Core development dependencies look good!$(NC)"

check-docker:
	@echo "$(CYAN)Checking Docker availability...$(NC)"
	@command -v docker >/dev/null 2>&1 || { echo "$(YELLOW)✗ Docker not installed$(NC)"; exit 1; }
	@echo "$(GREEN)✓ Docker installed$(NC)"
	@docker info >/dev/null 2>&1 || { echo "$(YELLOW)✗ Docker daemon not running$(NC)"; exit 1; }
	@echo "$(GREEN)✓ Docker daemon running$(NC)"
	@echo ""

check-deps: check-prereqs check-docker
	@echo "$(GREEN)All required dependencies are installed!$(NC)"

# ===================================================================
# Database
# ===================================================================

db-migrate:
	@echo "$(CYAN)Running database migrations...$(NC)"
	@poetry run alembic upgrade head

db-migrate-create:
	@echo "$(CYAN)Creating new migration...$(NC)"
	@read -p "Enter migration message: " msg; \
	poetry run alembic revision --autogenerate -m "$$msg"

db-seed:
	@echo "$(CYAN)Seeding database with test data...$(NC)"
	@poetry run python scripts/seed_data.py --env=development

db-reset:
	@echo "$(YELLOW)⚠ WARNING: This will reset the database!$(NC)"
	@read -p "Continue? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		poetry run alembic downgrade base && \
		poetry run alembic upgrade head && \
		make db-seed; \
	fi

# ===================================================================
# Testing
# ===================================================================

test:
	@echo "$(CYAN)Running all tests with coverage...$(NC)"
	@poetry run pytest --cov=src/dotmac --cov-report=term-missing --cov-report=xml

test-fast:
	@echo "$(CYAN)Running tests without coverage...$(NC)"
	@poetry run pytest -v --tb=short

lint:
	@echo "$(CYAN)Running Python linting...$(NC)"
	@poetry run ruff check src/ tests/

format:
	@echo "$(CYAN)Formatting Python code...$(NC)"
	@poetry run ruff check --fix src/ tests/
	@poetry run ruff format src/ tests/

# ===================================================================
# Build & Deploy
# ===================================================================

post-deploy-isp:
	@echo "$(CYAN)Running post-deployment setup for ISP backend...$(NC)"
	@./scripts/post-deploy.sh isp

build-isp:
	@echo "$(CYAN)Building ISP Docker images...$(NC)"
	@docker compose build

build-freeradius:
	@echo "$(CYAN)Building FreeRADIUS image for Apple Silicon...$(NC)"
	@docker build --platform linux/amd64 -f Dockerfile.freeradius -t freeradius-postgresql:latest .

docker-isp-up:
	@docker compose up -d isp-backend isp-frontend freeradius mongodb genieacs

docker-ps:
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
