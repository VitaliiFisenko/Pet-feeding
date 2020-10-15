IMAGE ?= backend:develop
CI_COMMIT_SHORT_SHA ?= $(shell git rev-parse --short HEAD)
GIT_STAMP ?= $(shell git describe)


.default: run

.EXPORT_ALL_VARIABLES:


run: COMPOSE ?= docker-compose -f compose-base.yml
run: docker-build
	$(COMPOSE) up -d


logs: COMPOSE ?= docker-compose -f compose-base.yml
logs:
	$(COMPOSE) logs -f api

stop: COMPOSE ?= docker-compose -f compose-base.yml
stop:
	$(COMPOSE) stop

docker-build:
	docker build --build-arg version=$(GIT_STAMP) -t $(IMAGE) .