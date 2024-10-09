# Task List Management System API

## Overview

This project is a task list management system built with FastAPI and PostgreSQL, enabling users to manage tasks (ToDo list)
and includes user authentication with JWT. The system allows users to create, update, view, and delete tasks. It
supports filtering by task status, and pagination, and ensures that only authorized users can access the service. The
application is fully Dockerized for easy setup and deployment.

API Documentation [Link](https://drive.google.com/file/d/1euuTm4GmwqqPT9e3e7NGLQs_kAPKqdP_/view?usp=sharing)

## Features

1. **FastAPI with PostgreSQL Setup**
2. **CRUD Operations for Managing Tasks**
   - Get a list of all tasks
   - Get a list of all user's tasks
   - Get information about a specific task
   - Create new task
   - Update task information (can be updated only by owner)
   - Delete a task (can be updated only by owner)
3. **Task Filtering and Pagination**
   - Filtering tasks by status (New, In progress, Completed)
5. **Docker Container with Docker Compose**
6. **JWT User Authentication and Authorization**
7. **Writing Unit Tests with Coverage**
8.  - Unit tests for API endpoints
    - Coverage tool to check the percentage of test coverage using
9. Unit tests for the main API endpoints
10. **Manage Migrations with Alembic**


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
