# Project Name: school_admin

## Description

This project provides a set of tools to manage a Django application using Docker and Docker Compose. The `Makefile` simplifies common development and deployment tasks.

## Prerequisites

-   Docker: Ensure Docker is installed on your system.
-   Docker Compose: Ensure Docker Compose is installed on your system.

## Makefile Overview

The `Makefile` defines a series of commands to help you manage the application. Here's a breakdown of each command:

### Core Commands

-   `make help`: Displays a help message with a list of available commands and their descriptions.
-   `make build`: Builds the Docker image for the Django application.
-   `make up`: Starts the Docker Compose services, including the Django application and any other dependencies (like the database).  Automatically builds the image before starting.
-   `make down`: Stops the Docker Compose services.
-   `make test`: Runs the Django tests inside the Docker container.  Starts the services before running the tests, and stops them afterward.
-   `make migrate`: Runs the Django database migrations.  Starts the services before running the migrations.
-   `make makemigrations`: Creates new Django database migrations. Starts the services before creating the migrations.
-   `make shell`: Opens a shell session inside the Django container, allowing you to interact with the application's environment. Starts the services before opening the shell.
-   `make rebuild`: Rebuilds the Docker image and restarts the Docker Compose services.
### Detailed Usage

1.  **Initial Setup**

    -   Clone the repository to your local machine.
    -   Ensure you have Docker and Docker Compose installed.

2.  **Using the Makefile**

    -   Open your terminal and navigate to the project's root directory (where the `Makefile` is located).

3.  **Available Commands**

    -   `make help`:
        ```bash
        make help
        ```
        Displays a list of available commands and their descriptions.

    -   `make build`:
        ```bash
        make build
        ```
        Builds the Docker image for the Django application. You need to run this command whenever there are changes in your `Dockerfile` or application code that require rebuilding the image.

    -   `make up`:
        ```bash
        make up
        ```
        Starts the Docker Compose services. This command will first build the Docker image (if necessary) and then start the containers defined in your `local.yml` (or the file defined by `COMPOSE_FILE`). This is the command you'll typically use to start your development environment.

    -   `make down`:
        ```bash
        make down
        ```
        Stops the Docker Compose services. This command stops the containers defined in your Docker Compose file.  Use this when you want to stop your development environment and free up resources.

    -   `make test`:
        ```bash
        make test
        ```
        Runs the Django tests. This command starts the Docker Compose services, runs the tests inside the `django` container, and then stops the services.  It's useful for verifying your application's functionality.

    -   `make migrate`:
        ```bash
        make migrate
        ```
        Applies any pending Django database migrations. This command starts the Docker Compose services, runs the `manage.py migrate` command inside the `django` container, and then stops the services.  Use this to update your database schema.

    -   `make makemigrations`:
        ```bash
        make makemigrations
        ```
        Creates new Django database migrations based on changes to your models. This command starts the Docker Compose services, runs the `manage.py makemigrations` command inside the `django` container, and then stops the services.

    -   `make shell`:
        ```bash
        make shell
        ```
        Opens a shell session inside the Django container. This is useful for debugging, running Django management commands, or inspecting the application's environment.

    -   `make rebuild`:
        ```bash
        make rebuild
        ```
        Rebuilds the Docker image and restarts the Docker Compose services.  This is useful when you've made changes to your Dockerfile or application code and want to ensure that the changes are reflected in your running containers.  It's a combination of `make down`, `make build`, and `make up`.

## Configuration

-   `PROJECT_NAME`:  Defines the name of the project (default: `school_admin`).
-   `IMAGE_NAME`: Defines the name of the Docker image (default: `$(PROJECT_NAME)`).
-   `COMPOSE_FILE`:  Specifies the Docker Compose file to use (default: `local.yml`).

You can customize these variables by creating a `.env` file in the project root directory and defining them there.  For example:

PROJECT_NAME=my_projectIMAGE_NAME=my_project_imageCOMPOSE_FILE=docker-compose.yml
## Docker Compose File (`local.yml`)

The `local.yml` file defines the services that make up your application, such as the Django application itself, the database, and any other dependencies.  You'll need to configure this file according to your project's requirements.  The `Makefile` uses this file to manage the services.
