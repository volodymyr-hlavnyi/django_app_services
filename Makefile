.PHONY: d-homework-i-run
# Make all actions needed for run homework from zero.
d-homework-i-run:
	@make init-configs &&\
	make d-run


.PHONY: d-homework-i-purge
# Make all actions needed for purge homework related data.
d-homework-i-purge:
	@make d-purge


.PHONY: init-configs
# Configuration files initialization
init-configs:
	@cp .env.homework .env && \
	cp docker-compose.override.dev.yml docker-compose.override.yml


.PHONY: d-run
# Just run
d-run:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		COMPOSE_PROFILES=full_dev \
		docker compose \
			up --build

.PHONY: d-run-i-local-dev
# Just run
d-run-i-local-dev:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		COMPOSE_PROFILES=local_dev \
		docker compose \
			up --build
		COMPOSE_PROFILES=full_dev \
		docker compose \
			up --build

.PHONY: d-run-i-pgadmin
# Run pgadmin
d-run-i-pgadmin:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		COMPOSE_PROFILES=pgadmin \
		docker compose \
			up --build

.PHONY: d-stop
# Stop services
d-stop:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		docker compose down


.PHONY: d-purge
# Purge all data related with services
d-purge:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
	COMPOSE_PROFILES=pgadmin   \
		docker compose down --volumes --remove-orphans --rmi local --timeout 0


.PHONY: init-dev
# Init environment for development
init-dev:
	@pip install --upgrade pip && \
	pip install --requirement requirements/local.txt && \
	pre-commit install


.PHONY: homework-i-run
# Run homework.
homework-i-run:
	@python run.py


.PHONY: homework-i-purge
homework-i-purge:
	@echo Goodbye


.PHONY: pre-commit-run
# Run tools for files from commit.
pre-commit-run:
	@pre-commit run


.PHONY: pre-commit-run-all
# Run tools for all files.
pre-commit-run-all:
	@pre-commit run --all-files


.PHONY: migrations
# Make migrations
migrations:
	@python manage.py makemigrations


.PHONY: migrate
# Migrate
migrate:
	@python manage.py migrate

.PHONY: homework-i-run-generate-contacts
# Run homework with generate 15 contacts.
homework-i-run-generate-contacts:
	@bash ./scripts/d-homework-i-run-contacts-generate.sh

.PHONY: homework-i-run-delete-contacts-all
# Run homework with delete all contacts.
homework-i-run-delete-contacts-all:
	@bash ./scripts/d-homework-i-run-contacts-delete-all.sh

.PHONY: init-dev-i-migrate-all
# Make migrations and make migrate together
init-dev-i-migrate-all:
	@python manage.py makemigrations && \
	python manage.py migrate

.PHONY: init-dev-i-create-superuser-cmd
# Create superuser
init-dev-i-create-superuser-cmd:
	@DJANGO_SUPERUSER_PASSWORD=admin123 python manage.py createsuperuser --user admin --email admin@gmail.com --no-input

.PHONY: init-dev-i-create-superuser
# Create superuser
init-dev-i-create-superuser:
	@python manage.py create_superuser

.PHONY: init-dev-i-delete-superuser
# Delete superuser
init-dev-i-delete-superuser:
	@python manage.py delete_superuser

#.PHONY: init-dev-i-generate-contacts
## init-dev-i-generate-contacts 20
#init-dev-i-generate-contacts:
#	@python manage.py generate_contacts --amount 20

#.PHONY: init-first-start-db
## Filling database for first use
#init-first-start-db:
#	@python manage.py init_first_start

