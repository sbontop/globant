IMAGE_NAME=myapp

.PHONY: dev
dev:
	@echo "Starting development environment..."
	docker-compose -f docker-compose.dev.yml down; \
	docker-compose -f docker-compose.dev.yml up 

.PHONY: prod
prod:
	@echo "Starting production environment..."
	docker-compose -f docker-compose.prod.yml down; \
	docker-compose -f docker-compose.prod.yml up

.PHONY: stop
down:
	@echo "Stopping containers..."
	docker-compose -f docker-compose.dev.yml down; \
	docker-compose -f docker-compose.prod.yml down

.PHONY: clean
clean:
	@echo "Cleaning up unused containers and images..."
	make down; \
	docker system prune -af

.PHONY: build-dev
build-dev:
	@echo "Building development image..."
	docker build -t $(IMAGE_NAME):dev -f Dockerfile.dev .

.PHONY: build-prod
build-prod:
	@echo "Building production image..."
	docker build -t $(IMAGE_NAME):prod -f Dockerfile.prod .

.PHONY: deploy
deploy:
	@echo "Deploying to production..."
	docker-compose -f docker-compose.prod.yml up --build -deploy

PHONY: test
test-dev:
	@echo "Running pytest unit tests within Django docker container..."
	docker-compose -f docker-compose.dev.yml run web pytest 

test-prod:
	@echo "Running pytest unit tests within Django docker container..."
	docker-compose -f docker-compose.prod.yml run web pytest