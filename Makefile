.PHONY: help test lint livedoc deploydoc clean install api-install eval-install update-deps setup-uv

GIT_ROOT ?= $(shell git rev-parse --show-toplevel)
PYTHON_VERSION ?= 3.9

help:   ## Show all Makefile targets.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'

test:	## Run the tests
	uv pytest pylate --durations=5 -n auto
	uv pytest tests --durations=5 -n auto

lint:	## Run linters: ruff
	uv run ruff check . --fix

livedoc:	## Create the docs
	uv python docs/parse
	uv mkdocs build --clean
	uv mkdocs serve --dirtyreload

deploydoc:	## Deploy the docs
	uv mkdocs gh-deploy --force

clean:  ## Clean up build artifacts.
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf dist
	rm -rf build
	rm -rf .venv

install:	## Install dev packages
	uv venv --python $(PYTHON_VERSION)
	uv pip install -e .[dev]

api-install:	## Install api packages
	uv venv --python $(PYTHON_VERSION)
	uv pip install .[api]

eval-install:	## Install eval packages
	uv venv --python $(PYTHON_VERSION)
	uv pip install .[eval]

update-deps:    ## Update dependencies.
	uv pip compile pyproject.toml -o requirements.txt
	uv pip sync requirements.txt
	uv run pre-commit autoupdate

setup-uv:   ## Setup uv with the specified version
	curl -LsSf https://astral.sh/uv/install.sh | sh -s
