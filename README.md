# Awesome sharer
## Requirements
- docker
- docker-compose
- make
## Setup app
```shell
# Build app, apply migrations and collect static
make build
# Run app
make or make run
# Show logs
make logs
```
## All commands
```shell
run:               Run application
stop:              Stop application
build:             Build application
rebuild:           Fresh build, apply migration, collect static
test:              Run tests
purge:             Clean up
logs:              Display logs
cli:               Open command line
collectstatic:     Collect static files
migrate:           Migrate database (optional param: app=app_name)
makemigrations:    Make new migrations (optional param: app=app_name)
startapp:          Create a new app required param: app=app_name
help:              Show this help.
```

## Live preview

## Postman collection
[link](Awesome-sharer.postman_collection.json)
