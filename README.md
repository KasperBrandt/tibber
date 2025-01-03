# Tibber

## Quick Start Instructions

### Local development
In order to run a local development server with a local Postgres database, run:
```
docker-compose --profile dev up --build
```

It's also possible to run `main.py` directly in order to debug within an IDE,
which would require connecting to an existing database and possibly changing the
existing configs values. 

### Running unit / integration tests
Running tests, which will also display coverage, can be done via:
```
docker-compose --profile test run test
```

### Loading in different configs
In order to load the production config, set environment variable ENV to prod and
then run the docker compose command:
```
ENV=prod docker-compose up -d
```

## Notes
- After initial implementation, added different algorithms to test performance for
large inputs when calculating intersections between x- and y-lines:
  - Binary search: takes ~5.2s, fastest based on unit tests and used by default
  - Simple intersection detection: takes ~7.5s
  - Early intersection filtering: takes ~7.9s
  - Interval tree: took ~25s, removed implementation
- Application runs on a simple development server, no gunicorn or nginx configurations
for running a production-like server have been added.

- All requirements have been added to the same file, which could be split up in requirements
needed for running the API and for running tests.
