POETRY ?= poetry
PYTHON ?= $(POETRY) run
HOST ?= 127.0.0.1
PORT ?= 8000
SRC ?= src/dotmac_isp
THIN_TESTS ?= tests/thin
IMAGE ?= dotmac-isp:candidate

.DEFAULT_GOAL := help

.PHONY: help toolchain lock-check lint format format-check type-check \
	legacy-check check test build image dev

help: ## List targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-18s %s\n", $$1, $$2}'

toolchain: ## Verify the exact Poetry version on every build surface
	python3 scripts/check_poetry_toolchain.py --active

lock-check: ## Validate the committed dependency lock without repairing it
	$(POETRY) check --lock

lint: ## Lint the thin runtime, controls, and their canaries
	$(PYTHON) ruff check $(SRC) scripts tests/thin

format: ## Format the thin runtime, controls, and their canaries
	$(PYTHON) ruff format $(SRC) scripts tests/thin

format-check: ## Check formatting
	$(PYTHON) ruff format --check $(SRC) scripts tests/thin

type-check: ## Strictly type-check public product/control surfaces
	$(PYTHON) mypy $(SRC) scripts

legacy-check: ## Prove the inherited tree did not drift silently
	python3 scripts/check_legacy_baseline.py

check: toolchain lock-check lint format-check type-check legacy-check ## Static gate

test: ## Thin-assembly and architecture canaries
	$(PYTHON) pytest --confcutdir=$(THIN_TESTS) $(THIN_TESTS) -q

build: ## Build the candidate wheel
	$(POETRY) build

image: ## Build the candidate container
	docker build --build-arg POETRY_VERSION=2.4.1 --tag $(IMAGE) .

dev: ## Run the candidate assembly locally
	$(PYTHON) uvicorn dotmac_isp.main:app --reload --host $(HOST) --port $(PORT)
