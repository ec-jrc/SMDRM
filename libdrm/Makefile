#################################
# Versioning
#################################
VERSION=1.0.0.dev20

#################################
# Install targets
#################################

.PHONY: install-dev
install-dev:
	@echo "+ $@"
	@pip install --upgrade pip black build pylint pytest twine
	@pip install .

.PHONY: pkg-deploy
pkg-deploy: version install-dev
	@echo "+ $@"
	@python3 -m build --sdist --wheel
	@twine check dist/libdrm-${VERSION}-*
	@twine upload --config-file ~/.pypirc --repository testpypi dist/libdrm-${VERSION}-*
	@rm -r dist/

.PHONY: pip-freeze
pip-freeze:
	@echo "+ $@"
	@pip freeze > ./requirements.freeze


#################################
# Test targets
#################################

.PHONY: elasticsearch-test
elasticsearch-test:
	@echo "+ $@"
	@docker run --rm --name elasticsearch-test -p "19200:19200" docker.elastic.co/elasticsearch/elasticsearch:7.14.0

.PHONY: unittests
unittests:
	@echo "+ $@"
	@pytest -v tests --ignore **/rabbitmq


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
	@pylint src/libdrm/**/*.py
	@pylint tests/**/*.py

.PHONY: code-format
code-format:
	@echo "+ $@"
	@black src/libdrm/**/*.py
	@black tests/**/*.py

.PHONY: repo-clean
repo-clean:
	@echo "+ $@"
	@rm -fr build **/*.egg-info .pytest_cache
