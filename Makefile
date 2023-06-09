SHELL := /bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:
.SILENT:

.DEFAULT_GOAL: help

.PHONY: help
help:
	@echo -e "Please use 'make <target>' where <target> is one of\n"
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "- \033[36m%-30s\033[0m %s\n", $$2, $$3}' | sort

.PHONY: install-dependencies  ## to install python dependencies
install-dependencies:
	pip install .

.PHONY: tests  ## to run tests
tests:
	pytest --html=report.html .
