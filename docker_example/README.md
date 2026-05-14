# Running HarxitFlow with Docker

This guide will help you get HarxitFlow up and running using Docker and Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Steps

1. Clone the HarxitFlow repository:

   ```sh
   git clone https://github.com/harxitflow-ai/harxitflow.git
   ```

2. Navigate to the `docker_example` directory:

   ```sh
   cd harxitflow/docker_example
   ```

3. Run the Docker Compose file:

   ```sh
   docker compose up
   ```

HarxitFlow will now be accessible at [http://localhost:7860/](http://localhost:7860/).

## Docker Compose Configuration

The Docker Compose configuration spins up two services: `harxitflow` and `postgres`.

### HarxitFlow Service

The `harxitflow` service uses the `harxitflowai/harxitflow:latest` Docker image and exposes port 7860. It depends on the `postgres` service.

Environment variables:

- `HARXITFLOW_DATABASE_URL`: The connection string for the PostgreSQL database.
- `HARXITFLOW_CONFIG_DIR`: The directory where HarxitFlow stores logs, file storage, monitor data, and secret keys.

Volumes:

- `harxitflow-data`: This volume is mapped to `/app/harxitflow` in the container.

### PostgreSQL Service

The `postgres` service uses the `postgres:16` Docker image and exposes port 5432.

Environment variables:

- `POSTGRES_USER`: The username for the PostgreSQL database.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
- `POSTGRES_DB`: The name of the PostgreSQL database.

Volumes:

- `harxitflow-postgres`: This volume is mapped to `/var/lib/postgresql/data` in the container.

## Switching to a Specific HarxitFlow Version

If you want to use a specific version of HarxitFlow, you can modify the `image` field under the `harxitflow` service in the Docker Compose file. For example, to use version 1.0-alpha, change `harxitflowai/harxitflow:latest` to `harxitflowai/harxitflow:1.0-alpha`.
