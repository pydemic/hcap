# Hospital Capacity

[![pipeline status](https://gitlab.com/pydemic/hcap/badges/master/pipeline.svg)](https://gitlab.com/pydemic/hcap/commits/master)
[![coverage report](https://gitlab.com/pydemic/hcap/badges/master/coverage.svg)](https://gitlab.com/pydemic/hcap/commits/master)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pydemic/hcap)

## Table of Contents

- [Hospital Capacity](#hospital-capacity)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Using rit tunnel](#using-rit-tunnel)
    - [Installation](#installation)
    - [Usage](#usage)
  - [Production Environment Variables](#production-environment-variables)
    - [CORS](#cors)
    - [Database](#database)
    - [Email](#email)
    - [Fake](#fake)
    - [Secrets](#secrets)
    - [Server](#server)
    - [Validations](#validations)

## Project Description

> TODO

## Using rit tunnel

### Installation

After installing [rit](https://gitlab.com/ritproject/cli#installation), config
your tunnel repo:

- Remotely:

  ```bash
  rit config tunnel add repo https://gitlab.com/pydemic/tunnel --name pydemic
  rit config tunnel default set pydemic --path .
  ```

- Locally:

  ```bash
  git clone https://gitlab.com/pydemic/tunnel ../tunnel
  rit config tunnel add local ../tunnel --name pydemic
  rit config tunnel default set pydemic --path .
  ```

### Usage

Examples of usage:

- If you use docker and docker-compose, you can:

  - Build the development image:

    ```bash
    rit tunnel run apps hcap development build
    ```

  - Fetch the development docker-compose:

    ```bash
    rit tunnel run apps hcap development fetch compose
    ```

  - Run the test pipeline:

    ```bash
    rit tunnel run apps hcap development test up
    rit tunnel run apps hcap development test sync
    rit tunnel run apps hcap development test all
    rit tunnel run apps hcap development test down
    ```

  - Start or shutdown PostgreSQL service:

    ```bash
    rit tunnel run services postgres up
    rit tunnel run services postgres down
    ```

  - Start or shutdown PostGis service:

    ```bash
    rit tunnel run services postgis up
    rit tunnel run services postgis down
    ```

  - Build the production image:

    ```bash
    rit tunnel run apps hcap production build
    ```

  - Fetch the production docker-compose:

    ```bash
    rit tunnel run apps hcap production fetch compose
    ```

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
