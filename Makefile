BACK_IMAGE ?= backend:develop
CI_COMMIT_SHORT_SHA ?= $(shell git rev-parse --short HEAD)
GIT_STAMP ?= $(shell git describe)


.default: run

.EXPORT_ALL_VARIABLES:


run-back: COMPOSE ?= docker-compose -f compose-back.yml
run-back: docker-build-back
	$(COMPOSE) up -d


logs-back: COMPOSE ?= docker-compose -f compose-back.yml
logs-back:
	$(COMPOSE) logs -f api

stop-back: COMPOSE ?= docker-compose -f compose-back.yml
stop-back:
	$(COMPOSE) stop

docker-build-back:
	docker build -f ./backend/Dockerfile --build-arg version=$(GIT_STAMP) -t $(BACK_IMAGE) .