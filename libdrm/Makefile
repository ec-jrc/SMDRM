#################################
# Versioning
#################################
VERSION=1.0.0.dev33

#################################
# Install targets
#################################

.PHONY: install-dev
install-dev:
	@echo "+ $@"
	@pip install --upgrade pip black build pylint pytest twine wheel
	@pip install .

.PHONY: pkg-deploy
pkg-deploy: version install-dev clean-repo
	@echo "+ $@"
	@python3 -m build --sdist --wheel
	@twine check dist/libdrm-${VERSION}-*
	@twine upload --config-file ~/.pypirc --repository testpypi dist/libdrm-${VERSION}-*

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
	@DISASTER_TYPE=floods pytest -v tests/


#################################
# Utilities
#################################

.PHONY: version
version:
	@echo "+ $@"
	@if [ -n "${VERSION}" ]; then echo "v${VERSION}"; else echo "Missing version"; exit 1; fi
	@sed -i "s/version=.*/version=\'${VERSION}\',/" ./setup.py

.PHONY: linter # https://vald-phoenix.github.io/pylint-errors/
linter:
	@echo "+ $@"
	@pylint *.py src/libdrm/**/*.py tests/**/*.py

.PHONY: pep-format
pep-format:
	@echo "+ $@"
	@black *.py src/libdrm/**/*.py tests/**/*.py

.PHONY: clean-repo
clean-repo:
	@echo "+ $@"
	@rm -fr build dist **/*.egg-info .pytest_cache
