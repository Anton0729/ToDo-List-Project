# Task List Management System API

## Overview

This project is a task management system built with FastAPI and PostgreSQL, enabling users to manage tasks (ToDo list)
and includes user authentication with JWT. The system allows users to create, update, view, and delete tasks. It
supports filtering by task status, and pagination, and ensures that only authorized users can access the service. The
application is fully Dockerized for easy setup and deployment.
API
Documentation [https://docs.google.com/document/d/1mFH4yAI1E3IzMou-yT8c5PPu1uHhQ_gV/edit?usp=sharing&ouid=110472722426617783568&rtpof=true&sd=true](https://docs.google.com/document/d/1bh7QTiMV3qM-nw91RlrzXImIhMehI2sc/edit?usp=sharing&ouid=110472722426617783568&rtpof=true&sd=true)

## Features

1. FastAPI with PostgreSQL setup
2. CRUD operations for managing tasks

- Create a book
- Retrieve a list of books
- Retrieve detailed information about a book by ID
- Update book information
- Delete a book

3. Task filtering and pagination
4. Docker container with docker-compose
5. JWT User Authentication and Authorization
6. Writing Unit Test with Coverage
7. Manage Migrations with Alembic script

## <ins> Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Anton0729/ToDo-List-Project.git
cd .\ToDo-List-Project\
```

### 2. Run Docker Desktop

### 3. Build the container

```bash
docker-compose build
```

### 4. Run the container

```bash
docker-compose up -d
```

### 5. Access the Application

- Application: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 6. Delete the container

```bash
docker-compose down
```

<br>

### Running Tests:

To run tests for this project, follow these steps:

### 1. Ensure the test database is created

Make sure the web container is running before creating the test database before running the tests. You can do this using
the following command:

```bash
docker-compose exec db psql -U postgres -c "CREATE DATABASE test_todo_db;"
```

### 2. Run the tests

Once the test database is set up, you can run the tests using the following command:

```bash
docker-compose run --rm web sh -c "pytest"
```

### 3. Test Coverage:

To check the test coverage, follow these steps:

```bash
docker-compose run --rm web sh -c "coverage run -m pytest && coverage report"
```
