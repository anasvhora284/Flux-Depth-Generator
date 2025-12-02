PYTHON ?= python3
VENV_DIR := .venv
PIP := $(VENV_DIR)/bin/pip
PY := $(VENV_DIR)/bin/python

.PHONY: env install build run clean test

env:
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Created virtualenv in $(VENV_DIR). Activate with 'source $(VENV_DIR)/bin/activate'"

install: env
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

build: install
	./scripts/build.sh

run: install
	$(PY) -m streamlit run app.py

test: install
	$(PY) -m pytest -q

clean:
	rm -rf dist build __pycache__ $(VENV_DIR)
