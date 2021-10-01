# versioning
VERSION=1.0.0.dev1

# environment
TARGET ?= "builder"

# docker env
DOCKER_HUB_USERNAME ?= "lucot"
IMAGE_NAME ?= "uploaderapi"


#################################
# Install targets
#################################

.PHONY: install-dev
install-dev:
	@echo "+ $@"
	@pip install --upgrade pip black pylint pytest
	@pip install -r requirements.txt

.PHONY: pip-freeze
pip-freeze:
	@echo "+ $@"
	@pip freeze > requirements.freeze


#################################
# Docker targets
#################################

.PHONY: clean-image
clean-image: version
	@echo "+ $@"
	@docker rmi $(docker images | grep ${IMAGE_NAME}) || true

.PHONY: image
image: version
	@echo "+ $@"
	@DOCKER_BUILDKIT=1 docker build --target ${TARGET} -t ${IMAGE_NAME}:${VERSION} .
	@docker tag ${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}:latest
	@docker images --format '{{.Repository}}:{{.Tag}}\tSize:{{.Size}}' | grep ${IMAGE_NAME}

.PHONY: push
push: clean-image image
	@echo "+ $@"
	@docker tag ${IMAGE_NAME}:latest ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest
	@docker tag ${IMAGE_NAME}:${VERSION} ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}
	@docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest
	@docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}


#################################
# Test targets
#################################

.PHONY: integration
integration: image
	@echo "+ $@"
	@docker run --rm -it --name uploader_api --env-file .env -p 6000:5000 ${IMAGE_NAME}


#################################
# Utilities
#################################

.PHONY: version
version:
	@echo "+ $@"
	@if [ -n "${VERSION}" ]; then echo "v${VERSION}" > VERSION.txt; else echo "Missing version"; exit 1; fi

.PHONY: linter # https://vald-phoenix.github.io/pylint-errors/
linter:
	@echo "+ $@"
	@pylint *.py

.PHONY: code-clean
code-clean:
	@echo "+ $@"
	@black *.py
