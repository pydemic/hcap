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

### Getting started

Clone the repo, create a virtualenve using `mkvirtualenv` or your tool of choice
and `pip install -e .`. This will setup a basic development environment using
Django's runserver and sqlite.

You can initialize, seed the database, start the development server using
standard Django management commands via `manage.py` or, perhaps more conveniently,
you may use invoke tasks to execute the most common chores

| Command               | Description                            |
| :-------------------- | :------------------------------------- |
| `inv db`              | Run makemigrations and migrate         |
| `inv db-fake`         | Seed database with users and fake data |
| `inv run`             | Start application                      |

You can list all options with `inv -l`.

The `inv db-fake` command creates a few useful users that you can use to interact
with the platform under different roles.

* **admin:** The superuser, e-mail: admin@admin.com, password: admin.
* **user:** A regular user that just sign up, e-mail: user@user.com, password: user.
* **notifier:** A user authorized to notify for a hospital, e-mail: notifier@notifier.com, password: notifier.
* **manager:** A user authorized manage notifiers for a given state, e-mail: manager@manager.com, password: manager.

It also populates the database with a few additional entries. The manager has a few
authorized and non-authorized notifiers to play with. The notifier is registered to
a healthcare unit and already has a small history of notifications.


### Getting started with Docker

If you prefer Docker ask someone in the dev team to fill up this section ;-)
There are lots of Docker enthusiasts in the team that use it for daily
development.

## Using rit tunnel

### Installation

After installing [rit](https://gitlab.com/ritproject/cli#installation), config
your tunnel repo either remotely,

```bash
rit config tunnel add repo https://gitlab.com/pydemic/tunnel --name pydemic
rit config tunnel default set pydemic --path .
```

or locally,

```bash
git clone https://gitlab.com/pydemic/tunnel ../tunnel
rit config tunnel add local ../tunnel --name pydemic
rit config tunnel default set pydemic --path .
```

### Usage

If you use docker and docker-compose, you use `rit` commands to automate several
processes. The table list the main options.

| Description                          | Commands                                                                                                                                                                                             |
| :----------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Build the development image          | `rit tunnel run apps hcap development build`                                                                                                                                                         |
| Fetch the development docker-compose | `rit tunnel run apps hcap development fetch compose`                                                                                                                                                 |
| Run the test pipeline                | `rit tunnel run apps hcap development test up<br>rit tunnel run apps hcap development test sync<br>rit tunnel run apps hcap development test all<br>>rit tunnel run apps hcap development test down` |
| Start or shutdown PostgreSQL service | `rit tunnel run services postgres up<br>rit tunnel run services postgres down`                                                                                                                       |
| Start or shutdown PostGis service    | `rit tunnel run services postgis up<br>rit tunnel run services postgis down`                                                                                                                         |
| Build the production image           | `rit tunnel run apps hcap production build`                                                                                                                                                          |
| Fetch the production docker-compose  | `rit tunnel run apps hcap production fetch compose`                                                                                                                                                  |

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
