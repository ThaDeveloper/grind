.PHONY: help
DOCKER_DEV_COMPOSE_FILE := docker/dev/docker-compose.yml
DOCKER_TEST_COMPOSE_FILE := docker/test/docker-compose.yml
DOCKER_PROD_COMPOSE_FILE := docker/prod/docker-compose.yml

DOCKER_PROD_PROJECT := "grind"
REPO_NAME := grind

# -f : access files outside the build context
MANAGE := docker-compose -f $(DOCKER_DEV_COMPOSE_FILE) run app python manage.py
DOCKER_DEV_COMPOSE := docker-compose -f $(DOCKER_DEV_COMPOSE_FILE)
DOCKER_TEST_COMPOSE := docker-compose -f $(DOCKER_TEST_COMPOSE_FILE)
DOCKER_PROD_COMPOSE := docker-compose -f $(DOCKER_PROD_COMPOSE_FILE) -p $(DOCKER_PROD_PROJECT)

# container repo
DOCKER_REGISTRY ?= ${DOCKER_REG}
# Repository Filter
REPO_FILTER := $(DOCKER_REGISTRY)/$(REPO_NAME)

dev:
	@${DOCKER_DEV_COMPOSE} up --build
migrations:
	@${MANAGE} makemigrations
migrate:
	@${MANAGE} migrate
run_dev:
	${INFO} "Starting Grind ..."
	@${DOCKER_DEV_COMPOSE} up
down:
	@${DOCKER_DEV_COMPOSE} down
db:
	@echo "Starting grind_db container..."
	@docker exec -it grind_db psql -U postgres
app:
	@echo "Start grind app service..."
	@${DOCKER_DEV_COMPOSE} run --rm app bash
test:
	${INFO} "Building required images for testing"
	@ echo " "
	@${DOCKER_TEST_COMPOSE} build --pull app
	${INFO} "Build Completed successfully"
	@ echo " "
	@ ${INFO} "Running tests in docker container"
	@${DOCKER_TEST_COMPOSE} up app
	${INFO} "Cleaning up test data ..."
	@${DOCKER_TEST_COMPOSE} down -v
grind_app:
	@ docker run -d -p 80:80 grind_app
grind_db:
	@ docker run -d -p 80:80 grind_db
prod:
	@ ${DOCKER_PROD_COMPOSE} up --build -d
tag:
	${INFO} "Tagging release image with tags $(TAG_ARGS)..."
	@ $(foreach tag,$(TAG_ARGS), docker tag $(IMAGE_ID) $(DOCKER_REGISTRY)/$(REPO_NAME):$(tag);)
	@echo " "
push:
	${INFO} "Publishing release image $(IMAGE_ID) to $(DOCKER_REGISTRY)/$(REPO_NAME)"
	@ $(foreach tag,$(shell echo $(REPO_EXPR)), docker push $(tag);)
	${SUCCESS} "Publish complete"
dangling:
	${INFO} "*Dangling images*"
	@ docker images -f dangling=true -q --no-trunc
clean:
	${INFO} "====> Cleaing docker env"
	@ $(DOCKER_DEV_COMPOSE) down -v
	@ docker images -f dangling=true -q --no-trunc -f label=application=grind | xargs -I ARGS docker rmi ARGS
	${INFO} "====> Clean complete"
#check make usage
help:
	@echo ''
	@echo 'Usage:'
	@echo '${YELLOW} make ${RESET} ${GREEN}<target> [options]${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		message = match(lastLine, /^## (.*)/); \
		if (message) { \
			command = substr($$1, 0, index($$1, ":")-1); \
			message = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} %s\n", command, message; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''

# get cmd make tag argument
# eg make tag 2019-12-21, arg is 2019-12-21
ifeq (tag,$(firstword $(MAKECMDGOALS)))
  TAG_ARGS := $(word 2, $(MAKECMDGOALS))
  ifeq ($(TAG_ARGS),)
    $(error You must specify a tag)
  endif
  $(eval $(TAG_ARGS):;@:)
endif

APP_CONTAINER_ID := $$($(DOCKER_PROD_COMPOSE) ps -q app)
IMAGE_ID := $$(docker inspect -f '{{ .Image }}' $(APP_CONTAINER_ID))
# Fech all image build tags
REPO_EXPR := $$(docker inspect -f '{{range .RepoTags}}{{.}} {{end}}' $(IMAGE_ID) | grep -o "$(REPO_FILTER)" | xargs )
 # COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)

NC := "\e[0m"
RESET  := $(shell tput -Txterm sgr0)
TARGET_MAX_CHAR_NUM=10

INFO := @bash -c 'printf $(YELLOW); echo "===> $$1"; printf $(NC)' SOME_VALUE
SUCCESS := @bash -c 'printf $(GREEN); echo "===> $$1"; printf $(NC)' SOME_VALUE