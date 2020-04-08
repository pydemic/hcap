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
    - [Secrets](#secrets)
    - [Server](#server)

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

### Secrets

| Name         | Default     | Pattern | Description                    |
| :----------- | :---------- | :------ | :----------------------------- |
| `SECRET_KEY` | Must be set | String  | Django's security entropy hash |

### Server

| Name             | Default | Pattern | Description                |
| :--------------- | :------ | :------ | :------------------------- |
| `SERVER_PORT`    | `8000`  | Integer | Server port                |
| `SERVER_WORKERS` | `1`     | Integer | Amount of gunicorn workers |
