.PHONY: clean clean-test clean-pyc clean-build docs help init
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys
for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-pyc clean-test ## remove all test, coverage and Python artifacts

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

init: ## installs all the requirements for dev env
	pip install -r requirements-dev.txt

venv-reset: ## resets current virtualenv to test a very clean test
	pip uninstall `pip freeze` -y
	make init

lint: ## check style with flake8
	pylint pychatbot

test: clean-pyc ## run tests quickly with the default Python
	pytest
	
test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source pychatbot -m pytest
		coverage report -m

