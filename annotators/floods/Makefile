# versioning
VERSION=1.0.0.dev1

# docker
TARGET ?= "builder"
DOCKER_HUB_USERNAME ?= "lucot"
IMAGE_NAME = "floodsapi"

# models directory
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
MODEL_DIR ?= ${ROOT_DIR}/models


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
	@pip freeze > ./requirements.freeze


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

.PHONY: unittests
unittests: image download-model download-laser
	@echo "+ $@"
	@docker run --rm -v ${MODEL_DIR}:/models ${IMAGE_NAME} pytest -v


#################################
# Utilities
#################################

.PHONY: version
version:
	@echo "+ $@"
	@if [ -n "${VERSION}" ]; then echo "v${VERSION}" > VERSION.txt; else echo "Missing version"; exit 1; fi

.PHONY: download-model
download-model:
	@echo "+ $@"
	@if [ ! -f "${MODEL_DIR}/current-model.json" ]; then\
		python download.py --output=${MODEL_DIR} --username=${BITBUCKET_USERNAME} --password=${BITBUCKET_PASSWORD}; \
	fi

.PHONY: download-laser
download-laser: install-dev
	@echo "+ $@"
	@if [ ! -f "${MODEL_DIR}/embeddings/93langs.fcodes" ]; then\
		mkdir -p ${MODEL_DIR}/embeddings && python -m laserembeddings download-models ${MODEL_DIR}/embeddings;\
	fi

.PHONY: linter # https://vald-phoenix.github.io/pylint-errors/
linter:
	@echo "+ $@"
	@pylint src/*.py tests/*.py

.PHONY: code-format
code-format:
	@echo "+ $@"
	@black src/*.py tests/*.py
