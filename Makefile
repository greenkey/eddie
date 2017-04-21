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

clean: clean-pyc clean-test clean-build ## remove all test, coverage and Python artifacts

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

clean-build: ## remove test and coverage artifacts
	rm -fr dist/

init: ## installs all the requirements for dev env
	pip install --upgrade pip
	pip install -r requirements-dev.txt

venv-reset: ## resets current virtualenv to test a very clean test
	virtualenv --clear $VIRTUAL_ENV
	make init

lint: ## check style with pylint
	pylint eddie

test: clean-pyc ## run tests quickly with the default Python
	pytest
	
test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source eddie -m pytest
	coverage report -m

complexity: ## list the list of too complex functions and methos
	python -m mccabe --min 7 `find eddie -name "*.py"` | sort -r -k 3

dist-test: clean-build # test-all ## build the package and upload
	python setup.py register -r https://testpypi.python.org/pypi
	git push --tags
	python setup.py sdist
	twine upload dist/* -r testpypi

dist-prod: clean-build # test-all ## build the package and upload
	python setup.py register -r https://pypi.python.org/pypi
	git push --tags
	python setup.py sdist
	twine upload dist/* -r pypi
