# https://github.com/sio/Makefile.venv
include Makefile.venv

.PHONY: help test run

VENV_NAME?=.venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
MAIN?=get_gcal_next_event.py

help:
	@echo "make:"
	@echo "    create venv and install requirements"
	@echo "make run:"
	@echo "    run bitbar script and print result"
	@echo "make test:"
	@echo "    run unittest"

.DEFAULT: venv show-venv
	@echo to activate the virtual environment in a shell
	@echo source .venv/bin/activate
	@echo or type make bash


test: $(PYTHON)
	$(VENV)/python -m unittest

run: $(PYTHON) $(MAIN)
	$(VENV)/python $(MAIN)
