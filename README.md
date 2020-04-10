# Hospital Capacity

[![pipeline status](https://gitlab.com/pydemic/capacidade_hospitalar/badges/master/pipeline.svg)](https://gitlab.com/pydemic/capacidade_hospitalar/commits/master)
[![coverage report](https://gitlab.com/pydemic/capacidade_hospitalar/badges/master/coverage.svg)](https://gitlab.com/pydemic/capacidade_hospitalar/commits/master)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pydemic/capacidade_hospitalar)

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

After installing [rit](https://gitlab.com/ritproject/cli#installation), config your tunnel repo:

- Remotely:

  ```bash
  rit config tunnel add repo https://github.com/pydemic/tunnel --name pydemic
  rit config tunnel default set pydemic --path .
  ```

- Locally:

  ```bash
  git clone https://github.com/pydemic/tunnel ../tunnel
  rit config tunnel add local ../tunnel --name pydemic
  rit config tunnel default set pydemic --path .
  ```

### Usage

Examples of usage:

- If you use docker and docker-compose, you can:

  - Build the development image:

    ```bash
    rit tunnel run apps hospital_capacity development build
    ```

  - Fetch the development docker-compose:

    ```bash
    rit tunnel run apps hospital_capacity development fetch compose
    ```

  - Run the test pipeline:

    $ rit tunnel run apps hospital_capacity development test up
    $ rit tunnel run apps hospital_capacity development test sync
    $ rit tunnel run apps hospital_capacity development test all
    $ rit tunnel run apps hospital_capacity development test down

  - Build the production image:

    $ rit tunnel run apps hospital_capacity production build

  - Fetch the production docker-compose:

    $ rit tunnel run apps hospital_capacity production fetch compose

## Production Environment Variables

### CORS

| Name                | Default    | Pattern         | Description                           |
| :------------------ | :--------- | :-------------- | :------------------------------------ |
| `HC__ALLOWED_HOSTS` | Empty list | List of Strings | Set allowed hosts to serve the system |

### Database

| Name                    | Default     | Pattern                | Description                                                            |
| :---------------------- | :---------- | :--------------------- | :--------------------------------------------------------------------- |
| `HC__DATABASE_TYPE`     | `sqlite`    | `sqlite`, `postgresql` | Set project DBMS                                                       |
| `HC__POSTGRES_DB`       | `hcapacity` | String                 | If `HC__DATABASE_TYPE` is `postgresql`, set database name              |
| `HC__POSTGRES_HOST`     | `postgres`  | String                 | If `HC__DATABASE_TYPE` is `postgresql`, set database hostname          |
| `HC__POSTGRES_PASSWORD` | `hcapacity` | String                 | If `HC__DATABASE_TYPE` is `postgresql`, set database username password |
| `HC__POSTGRES_PORT`     | `5432`      | Integer                | If `HC__DATABASE_TYPE` is `postgresql`, set database port              |
| `HC__POSTGRES_USER`     | `hcapacity` | String                 | If `HC__DATABASE_TYPE` is `postgresql`, set database username          |

### Email

| Name                      | Default                                   | Pattern                   | Description                                           |
| :------------------------ | :---------------------------------------- | :------------------------ | :---------------------------------------------------- |
| `HC__DEFAULT_FROM_EMAIL`  | `you@domain.com`                          | String                    | Set default email sender                              |
| `HC__EMAIL_HOST`          | Must be set if `HC__EMAIL_MODE` is `smtp` | String                    | If `HC__EMAIL_MODE` is `smtp`, set SMTP host          |
| `HC__EMAIL_HOST_PASSWORD` | Must be set if `HC__EMAIL_MODE` is `smtp` | String                    | If `HC__EMAIL_MODE` is `smtp`, set SMTP user password |
| `HC__EMAIL_HOST_USER`     | Must be set if `HC__EMAIL_MODE` is `smtp` | String                    | If `HC__EMAIL_MODE` is `smtp`, set SMTP user          |
| `HC__EMAIL_MODE`          | `console`                                 | `smtp`, `console`, `file` | Select email backend                                  |
| `HC__EMAIL_PORT`          | `587`                                     | Integer                   | If `HC__EMAIL_MODE` is `smtp`, set SMTP port          |

### Fake

| Name                      | Default | Pattern | Description                                               |
| :------------------------ | :------ | :------ | :-------------------------------------------------------- |
| `HC__FAKE_ADMIN_PASSWORD` | `admin` | String  | Set admin password generated by "createfakeusers" command |
| `HC__FAKE_USER_PASSWORD`  | `user`  | String  | Set user password generated by "createfakeusers" command  |

### Secrets

| Name             | Default    | Pattern | Description                    |
| :--------------- | :--------- | :------ | :----------------------------- |
| `HC__SECRET_KEY` | `changeme` | String  | Django's security entropy hash |

### Server

| Name          | Default     | Pattern | Description                |
| :------------ | :---------- | :------ | :------------------------- |
| `HC__HOST`    | `127.0.0.1` | String  | Server host                |
| `HC__PORT`    | `8000`      | Integer | Server port                |
| `HC__WORKERS` | `1`         | Integer | Amount of gunicorn workers |

### Validations

| Name               | Default | Pattern | Description                                                              |
| :----------------- | :------ | :------ | :----------------------------------------------------------------------- |
| `HC__VALIDATE_CPF` | `True`  | Boolean | If `True`, validate Brazilian social security number verification digits |
