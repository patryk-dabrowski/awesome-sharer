.PHONY: run stop build rebuild test purge logs cli collectstatic migrate makemigrations startapp help

run:						## Run application
	docker-compose up -d

stop:						## Stop application
	docker-compose down

build: migrate collectstatic			## Build application, apply migration, collect static
	docker-compose build

rebuild: purge build				## Fresh build

test:						## Run tests
	docker-compose run --rm web python manage.py test

purge:						## Clean up
	docker-compose down --remove-orphans --rmi local -v

logs:						## Display logs
	docker-compose logs -ft --tail 50

cli:						## Open command line
	docker-compose run --rm web sh

collectstatic:					## Collect static files
	docker-compose run --rm web python manage.py collectstatic --no-input --clear

migrate:					## Migrate database (optional param: app=app_name)
	docker-compose run --rm web python manage.py migrate $(value $1)

makemigrations:					## Make new migrations (optional param: app=app_name)
	docker-compose run --rm web python manage.py makemigrations $(app)

startapp:					## Create a new app required param: app=app_name
	docker-compose run --rm web python manage.py startapp "$${app:?param app is required}"

help:						## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
