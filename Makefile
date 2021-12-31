export PROJECTNAME=$(shell basename "$(PWD)")

.SILENT: ;               # no need for @

black: ## Runs black for code formatting
	black twitils --exclude generated

setup: clean ## Re-initiates virtualenv
	rm -rf venv
	python3 -m venv venv
	./venv/bin/python3 -m pip install -r requirements.txt

deps: ## Reinstalls dependencies
	./venv/bin/python3 -m pip install -r requirements.txt

clean: ## Clean package
	rm -rf build dist

local: black ## Run local main
	./venv/bin/python3 local_main.py

tests: clean ## Run all unit tests
	export PYTHONPATH=`pwd`:$PYTHONPATH && ./venv/bin/pytest tests

package: clean
	./pypi.sh

.PHONY: help
.DEFAULT_GOAL := help

help: Makefile
	echo
	echo " Choose a command run in "$(PROJECTNAME)":"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo