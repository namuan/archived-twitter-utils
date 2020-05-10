export PROJECTNAME=$(shell basename "$(PWD)")

.SILENT: ;               # no need for @

black: ## Runs black for code formatting
	black twitils --exclude generated

clean: ## Clean package
	rm -rf build dist

test: black ## Run all unit tests
	export PYTHONPATH=`pwd`:$PYTHONPATH && pytest tests

package: test
	./pypi.sh

.PHONY: help
.DEFAULT_GOAL := help

help: Makefile
	echo
	echo " Choose a command run in "$(PROJECTNAME)":"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo