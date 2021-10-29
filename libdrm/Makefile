#################################
# Install targets
#################################

.PHONY: install-dev
install-dev:
	@echo "+ $@"
	@pip install .

.PHONY: pip-freeze
pip-freeze:
	@echo "+ $@"
	@pip freeze > requirements.txt


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

.PHONY: publish
publish:
	@echo "+ $@"
	@python -m pip install --upgrade build twine
	@python -m build
	@python -m twine check dist/libdrm-*
	@python -m twine upload -u __token__ --repository testpypi dist/libdrm-*
	@rm -r dist/ build/ .pytest_cache/ **/*.egg-info
