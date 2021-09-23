#################################
# Versioning
#################################
VERSION=0.1

#################################
# Install targets
#################################

.PHONY: install-dev
install-dev:
	@echo "+ $@"
	@pip install .
	@pip install black pylint pytest

.PHONY: pip-freeze
pip-freeze:
	@echo "+ $@"
	@pip freeze > ./requirements.freeze


#################################
# Test targets
#################################

.PHONY: unittests
unittests:
	@echo "+ $@"
	@pytest -v tests


#################################
# Utilities
#################################

.PHONY: version
version:
	@echo "+ $@"
	@if [ -n "${VERSION}" ] ; then echo "v${VERSION}" ; else echo "Missing version"; exit 1 ; fi
	@sed -i "s/version=.*/version=\'${VERSION}\',/" ./setup.py

.PHONY: linter # https://vald-phoenix.github.io/pylint-errors/
linter:
	@echo "+ $@"
	@pylint **/*.py

.PHONY: code-format
code-format:
	@echo "+ $@"
	@black **/*.py
