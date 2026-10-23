
# devops-capstone-project

A Customer Accounts microservice project using Python, Flask, and REST APIs. The project includes account management, test-driven development, automated testing, continuous integration, security, Docker containerization, Kubernetes deployment, and continuous delivery.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-green.svg)](https://shields.io/)

This repository contains the starter code for the project in [**IBM-CD0285EN-SkillsNetwork DevOps Capstone Project**](https://www.coursera.org/learn/devops-capstone-project?specialization=devops-and-software-engineering), which is part of the [**IBM DevOps and Software Engineering Professional Certificate**](https://www.coursera.org/professional-certificates/devops-and-software-engineering).

## Usage

Use this repository as the starting point for your DevOps Capstone project. It contains the code needed to develop the Customer Accounts microservice.

Do not fork the original repository. Create your own repository using GitHub's **Use this template** button. This copies the starter code into your repository without creating a fork relationship.

## Development Environment

These labs are designed to be executed in the IBM Developer Skills Network Cloud IDE with OpenShift. Use the links provided in the Coursera Capstone project to access the lab environment.

Initialize the environment by sourcing `bin/setup.sh`. Do not run it as a standalone Bash script because it sets environment variables.

```bash
source bin/setup.sh
```

This installs Python 3.9, makes it the default Python version, modifies the terminal prompt, creates a Python virtual environment, and activates it.

After setup, your prompt should look similar to:

```bash
(venv) theia:project$
```

## Useful Commands

These commands are normally performed automatically during setup but may be useful if something goes wrong.

### Activate the Python 3.9 Virtual Environment

```bash
source ~/venv/bin/activate
```

### Install Python Dependencies

Make sure the Python virtual environment is activated, then run:

```bash
make install
```

### Start the PostgreSQL Docker Container

If the PostgreSQL service is unavailable, run:

```bash
make db
```

Check whether PostgreSQL is running:

```bash
docker ps
```

## Project Layout

The microservice code is contained in the `service` package. Tests are located in the `tests` folder. The code follows the Model-View-Controller pattern, with database code and business logic in `models.py` and REST API routing in `routes.py`.

```text
├── service
│   ├── common/
│   ├── config.py
│   ├── models.py
│   └── routes.py
├── setup.cfg
└── tests
    ├── factories.py
    ├── test_cli_commands.py
    ├── test_models.py
    └── test_routes.py
```

## Data Model

The Account model contains the following fields:

| Name | Type | Optional |
|---|---|---|
| id | Integer | False |
| name | String(64) | False |
| email | String(64) | False |
| address | String(256) | False |
| phone_number | String(32) | True |
| date_joined | Date | False |

## Your Task

Complete the Customer Accounts microservice by implementing the REST APIs for `READ`, `UPDATE`, `DELETE`, and `LIST`, while maintaining **95% code coverage**.

Follow Test-Driven Development (TDD): first write tests for the functionality you want, then implement the code required to make those tests pass.

The project will also include automated testing, continuous integration, security headers, CORS policies, Docker containerization, Kubernetes deployment, and an automated continuous delivery pipeline.

## Local Kubernetes Development

This repository can also be used for local Kubernetes development. The following commands are intended to simulate the Cloud IDE environment locally and are not recommended for execution in the Cloud IDE.

At a minimum, install [Docker Desktop](https://www.docker.com/products/docker-desktop). For the full development environment, install [Visual Studio Code](https://code.visualstudio.com) and the [Remote Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

### 1. Start a Local K3D Kubernetes Cluster

```bash
make cluster
```

### 2. Install Tekton

```bash
make tekton
```

### 3. Install the ClusterTasks

```bash
make clustertasks
```

These commands prepare a local environment for Tekton development.

## Author

[John Rofrano](https://www.coursera.org/instructor/johnrofrano), Senior Technical Staff Member, DevOps Champion, IBM Research, and Coursera instructor.

## License

Licensed under the Apache License. See [LICENSE](LICENSE).

<h3 align="center">© IBM Corporation 2022. All rights reserved.</h3>
