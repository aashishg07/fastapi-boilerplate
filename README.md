# FastAPI Boilerplate Setup

This guide will help you set up the FastAPI application with PostgreSQL using Docker for local development.

## Prerequisites

Ensure you have the following installed:
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup Instructions

Follow these steps to set up your development environment:

1. **Copy the `docker-compose.local.yml` to the root directory as `docker-compose.yml`:**

   ```bash
   cp docker/docker-compose.local.yml docker-compose.yml
   ```

2. **Copy the `env_sample` file to `.env` in the root directory:**

   ```bash
   cp env_sample .env
   ```

   Update the `.env` file with the appropriate environment variables, such as database credentials.

3. **Build and start the containers:**

   Run the following command to build the Docker containers and start them in the background:

   ```bash
   docker compose up -d --build
   ```

   This will start the FastAPI app and the PostgreSQL database. The app will be accessible at [http://localhost:8000](http://localhost:8000).

## Stopping the Containers

To stop the running containers, use the following command:

```bash
docker compose down
```

This will stop and remove all the containers created by `docker compose up`.

## Viewing Logs

To view the logs of the FastAPI application, use the following command:

```bash
docker compose logs -f fastapi
```

For viewing PostgreSQL logs, use this command:

```bash
docker compose logs -f db
```

## Troubleshooting

If you encounter any issues during setup, check the logs for more details. You can also try restarting the containers or rebuilding the images.

```bash
docker compose up -d --build --force-recreate
```

---

That's it! You're good to go and can start developing your FastAPI app with PostgreSQL on Docker.


## Alembic Migration
#### OUT OF DOCKER-ENTRYPOINT SCRIPT !!!

If the migration fails or you need to generate new migration files, follow these steps:

1. To generate a new Alembic migration, use:

   ```bash
   alembic revision --autogenerate -m "<message>"
   ```
2. After running this command, execute the following to apply the migration files and make actual changes to the database:
  ```bash
  alembic upgrade head
  ```
