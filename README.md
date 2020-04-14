# Hospital Capacity

[![pipeline](https://gitlab.com/pydemic/hcap/badges/master/pipeline.svg)](https://gitlab.com/pydemic/hcap/commits/master)
[![coverage](https://gitlab.com/pydemic/hcap/badges/master/coverage.svg)](https://gitlab.com/pydemic/hcap/commits/master)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pydemic/hcap)

## Table of Contents

- [Hospital Capacity](#hospital-capacity)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Development](#development)
    - [Getting started](#getting-started)
    - [Setup with virtualenv](#setup-with-virtualenv)
    - [Setup with docker and docker compose](#setup-with-docker-and-docker-compose)
  - [Production Environment Variables](#production-environment-variables)
    - [CORS](#cors)
    - [Database](#database)
    - [Email](#email)
    - [Fake](#fake)
    - [Grafana](#grafana)
    - [Secrets](#secrets)
    - [Server](#server)
    - [Validations](#validations)

## Project Description

> TODO

## Development

### Getting started

- Start by cloning the project:

  ```bash
  # HTTPS
  git clone https://github.com/pydemic/hcap.git

  # SSH
  git@github.com:pydemic/hcap.git
  ```

- Set your development environment with:

  - [virtualenv](#setup-with-virtualenv)

  - [docker and docker-compose](#setup-with-docker-and-docker-compose)

  - Another setup of your choice

- Install/fetch the development dependencies:

  ```bash
  pip install -e .[dev]
  ```

- Seed the database with fake data:

  ```bash
  inv db-fake
  ```

- Start the application (the system will be available at <http://localhost:8000>):

  ```bash
  # With inv
  inv run

  # With manage.py
  python manage.py start

  # With hcap reference
  hcap start
  ```

- The `inv db-fake` command creates a few useful users from which you can use to interact with the
  platform under different roles:

  | Role     | E-mail                | Password | Description                                            |
  | :------- | :-------------------- | :------- | :----------------------------------------------------- |
  | Admin    | admin@admin.com       | admin    | Staff with superuser privileges                        |
  | User     | user@user.com         | user     | User that just signed up                               |
  | Notifier | notifier@notifier.com | notifier | User authorized to notify for hospitals                |
  | Manager  | manager@manager.com   | manager  | User authorized to manage notifiers from a given state |

- The `inv db-fake` command also populate the database with a few additional entries:

  - The manager has a few authorized and non-authorized notifiers to play with

  - The notifier is registered to a healthcare unit and already has a small history of notifications

- To list additional tasks or commands:

  ```bash
  # invoke tasks
  inv -l

  # manage.py commands
  python manage.py

  # hcap reference commands
  hcap
  ```

### Setup with virtualenv

Create a virtualenv using `mkvirtualenv` or another tool of your choice.

After that, you can continue the [getting started](getting-started) section normally.

### Setup with docker and docker compose

An updated `docker-compose.yml` for development can be found at:

- <https://gitlab.com/pydemic/tunnel/-/blob/master/apps/hcap/development/fetch/docker-compose.yml>.

If you use [VSCode](https://code.visualstudio.com/) and
[ms-vscode-remote.remote-containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
extension, a `.devcontainer` settings can be found at:

- <https://gitlab.com/pydemic/tunnel/-/tree/master/apps/hcap/development/fetch/vscode/.devcontainer>.

The `hcap` service starts idle, simply access the service terminal:

  ```bash
  # With docker-compose
  docker-compose exec hcap bash

  # With docker
  docker exec -it hcap bash
  ```

After that, you can continue the [getting started](getting-started) section normally.

## Production Environment Variables

### CORS

| Name                  | Default    | Pattern         | Description                           |
| :-------------------- | :--------- | :-------------- | :------------------------------------ |
| `HCAP__ALLOWED_HOSTS` | Empty list | List of Strings | Set allowed hosts to serve the system |

### Database

| Name                      | Default    | Pattern                | Description                                                              |
| :------------------------ | :--------- | :--------------------- | :----------------------------------------------------------------------- |
| `HCAP__DATABASE_TYPE`     | `sqlite`   | `sqlite`, `postgresql` | Set project DBMS                                                         |
| `HCAP__POSTGRES_DB`       | `hcap`     | String                 | If `HCAP__DATABASE_TYPE` is `postgresql`, set database name              |
| `HCAP__POSTGRES_HOST`     | `postgres` | String                 | If `HCAP__DATABASE_TYPE` is `postgresql`, set database hostname          |
| `HCAP__POSTGRES_PASSWORD` | `pydemic`  | String                 | If `HCAP__DATABASE_TYPE` is `postgresql`, set database username password |
| `HCAP__POSTGRES_PORT`     | `5432`     | Integer                | If `HCAP__DATABASE_TYPE` is `postgresql`, set database port              |
| `HCAP__POSTGRES_USER`     | `pydemic`  | String                 | If `HCAP__DATABASE_TYPE` is `postgresql`, set database username          |

### Email

| Name                        | Default                                     | Pattern                   | Description                                             |
| :-------------------------- | :------------------------------------------ | :------------------------ | :------------------------------------------------------ |
| `HCAP__DEFAULT_FROM_EMAIL`  | `you@domain.com`                            | String                    | Set default email sender                                |
| `HCAP__EMAIL_HOST`          | Must be set if `HCAP__EMAIL_MODE` is `smtp` | String                    | If `HCAP__EMAIL_MODE` is `smtp`, set SMTP host          |
| `HCAP__EMAIL_HOST_PASSWORD` | Must be set if `HCAP__EMAIL_MODE` is `smtp` | String                    | If `HCAP__EMAIL_MODE` is `smtp`, set SMTP user password |
| `HCAP__EMAIL_HOST_USER`     | Must be set if `HCAP__EMAIL_MODE` is `smtp` | String                    | If `HCAP__EMAIL_MODE` is `smtp`, set SMTP user          |
| `HCAP__EMAIL_MODE`          | `console`                                   | `smtp`, `console`, `file` | Select email backend                                    |
| `HCAP__EMAIL_PORT`          | `587`                                       | Integer                   | If `HCAP__EMAIL_MODE` is `smtp`, set SMTP port          |

### Fake

| Name                        | Default | Pattern | Description                                               |
| :-------------------------- | :------ | :------ | :-------------------------------------------------------- |
| `HCAP__FAKE_ADMIN_PASSWORD` | `admin` | String  | Set admin password generated by "createfakeusers" command |
| `HCAP__FAKE_USER_PASSWORD`  | `user`  | String  | Set user password generated by "createfakeusers" command  |

### Grafana

| Name                          | Default                 | Pattern | Description           |
| :---------------------------- | :---------------------- | :------ | :-------------------- |
| `HCAP__GRAFANA_DASHBOARD_UID` | `OMynCUCWx`             | String  | Grafana dashboard UID |
| `HCAP__GRAFANA_URL`           | `http://localhost:3000` | String  | Grafana URL           |

### Secrets

| Name               | Default    | Pattern | Description                    |
| :----------------- | :--------- | :------ | :----------------------------- |
| `HCAP__SECRET_KEY` | `changeme` | String  | Django's security entropy hash |

### Server

| Name            | Default     | Pattern | Description                |
| :-------------- | :---------- | :------ | :------------------------- |
| `HCAP__HOST`    | `127.0.0.1` | String  | Server host                |
| `HCAP__PORT`    | `8000`      | Integer | Server port                |
| `HCAP__WORKERS` | `1`         | Integer | Amount of gunicorn workers |

### Validations

| Name                 | Default | Pattern | Description                                                              |
| :------------------- | :------ | :------ | :----------------------------------------------------------------------- |
| `HCAP__VALIDATE_CPF` | `True`  | Boolean | If `True`, validate Brazilian social security number verification digits |
