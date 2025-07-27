PYTHON=$(shell which python3 )
VERSION=`cat cronzimus/VERSION`

# Check for UV installation
UV=$(shell which uv 2>/dev/null)
USE_UV=$(if $(UV),true,false)

ifeq (, $(PYTHON))
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

PYTHON_VERSION_MIN=3.10
PYTHON_VERSION_OK=$(shell $(PYTHON) -c 'from sys import version_info as v; v_min=int("".join("$(PYTHON_VERSION_MIN)".split("."))); print(0) if int(str(v.major)+str(v.minor)) >= v_min else print(1)')
PYTHON_VERSION=$(shell $(PYTHON) -c 'import sys; print("%d.%d"% sys.version_info[0:2])' )

PIP=$(PYTHON) -m pip
PYDOC=pydoc3

ifeq ($(PYTHON_VERSION_OK),1)
  $(error "Requires Python >= $(PYTHON_VERSION_MIN) - Installed: $(PYTHON_VERSION)")
endif

help: ## Print help for each target
	$(info Cronzimus - Task Scheduler and Job Manager)
	$(info ==========================================)
	$(info )
	$(info Available commands:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'
	$(info )
	$(info UV Support: $(USE_UV))
	@if [ "$(USE_UV)" = "true" ]; then \
		echo "UV is installed. Use 'make uv-install' for faster dependency installation."; \
	else \
		echo "UV not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
	fi

.PHONY: install
install: ## Installs dependencies (uses UV if available).
	@if [ "$(USE_UV)" = "true" ]; then \
		echo "Installing dependencies with UV..."; \
		$(UV) pip install -r requirements.txt; \
	else \
		echo "Installing dependencies with pip..."; \
		$(PIP) install -r requirements.txt; \
	fi

.PHONY: uv-install
uv-install: ## Install dependencies using UV (fast).
	@if [ "$(USE_UV)" = "true" ]; then \
		$(UV) pip install -r requirements.txt; \
	else \
		echo "UV not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	fi

.PHONY: uv-sync
uv-sync: ## Sync dependencies from pyproject.toml using UV.
	@if [ "$(USE_UV)" = "true" ]; then \
		$(UV) pip sync pyproject.toml; \
	else \
		echo "UV not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	fi

.PHONY: uv-venv
uv-venv: ## Create virtual environment using UV.
	@if [ "$(USE_UV)" = "true" ]; then \
		$(UV) venv; \
		echo "Virtual environment created. Activate with: source .venv/bin/activate"; \
	else \
		echo "UV not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	fi

.PHONY: run
run: ## Run the cronzimus for all vehicles.
	PYTHONPATH="." $(PYTHON) cronzimus/app.py

.PHONY: clean
clean: ## Remove the python binary files.
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	rm -rf build dist *.egg-info .pytest_cache cov_html .coverage htmlcov

.PHONY: lint
lint: ## Lint the code
	flake8

.PHONY: test
test: dev-install pytest code-analysis

.PHONY: dev-install
dev-install: ## Install testing in development mode.
	@if [ "$(USE_UV)" = "true" ]; then \
		echo "Installing dev dependencies with UV..."; \
		$(UV) pip install -e ".[dev]"; \
	else \
		echo "Installing dev dependencies with pip..."; \
		$(PIP) install -r requirements.txt; \
	fi

.PHONY: pytest
pytest: ## Tests the code base and creates code coverage report.
	$(PYTHON) -m pytest tests

.PHONY: check-black
check-black: ## Formats and checks code quality standards.
	$(PYTHON) -m black --check cronzimus/
	$(PYTHON) -m black --check tests/

PHONY: check-isort
check-isort:
	$(PYTHON) -m isort --profile black cronzimus --check-only
	$(PYTHON) -m isort --profile black tests --check-only

.PHONY: code-analysis
code-analysis: check-black check-isort

doc: ## Document the code
	@$(PYDOC) cronzimus

.PHONY: format
format: ## Format code with black and isort
	$(PYTHON) -m black cronzimus/ tests/
	$(PYTHON) -m isort --profile black cronzimus tests

.PHONY: security
security: ## Run security checks with bandit
	$(PYTHON) -m bandit -r cronzimus -ll

.PHONY: build
build: ## Build the package
	@if [ "$(USE_UV)" = "true" ]; then \
		echo "Building with UV..."; \
		$(UV) build; \
	else \
		echo "Building with pip..."; \
		$(PIP) install build; \
		$(PYTHON) -m build; \
	fi

.PHONY: install-uv
install-uv: ## Install UV package manager
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo "UV installed. Please restart your shell or run: source ~/.bashrc"

