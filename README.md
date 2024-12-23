# Tibber

## Quick Start Instructions

In order to run a local development server with a local Postgres database, run:
```
docker-compose --profile dev up --build  
```

Running tests, which will also display coverage, can be done via:
```
docker-compose --profile test run test
```

In order to load the production config, set environment variable ENV to prod and
then run the docker compose command:
```
ENV=prod docker-compose up -d
```

## Notes
- Application runs on a simple development server, no gunicorn or nginx configurations
for running a production-like server have been added.

- All requirements have been added to the same file, which could be split up in requirements
needed for running the API and for running tests.