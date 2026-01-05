# Spy Cat Agency – Backend API

This repository contains the backend implementation for the **Spy Cat Agency (SCA)** management system.  
It is a RESTful API built with **FastAPI** that allows the agency to manage spy cats, missions, and mission targets.

The API demonstrates CRUD operations, business rule enforcement, database interactions, and third-party API integration.

---

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- TheCatAPI (for breed validation)

---

## Features

### Spy Cats
- Create a spy cat (with breed validation)
- List all spy cats
- Retrieve a single spy cat
- Update a spy cat’s salary
- Delete a spy cat (only if not assigned to a mission)

### Missions & Targets
- Create missions with 1–3 targets in a single request
- Assign available cats to missions
- Update target notes and completion state
- Automatically complete missions when all targets are completed
- Prevent updates to completed targets or missions
- Prevent deletion of assigned missions

---

## Business Rules Enforced

- A cat can only have one mission at a time
- A mission must contain between 1 and 3 targets
- Target notes are locked once the target or mission is completed
- Missions cannot be deleted once assigned
- Cats cannot be deleted while assigned to a mission
- Cat breeds are validated against TheCatAPI

---

## Project Structure

    app/
    ├── main.py
    ├── database.py
    ├── deps.py
    ├── models.py
    ├── schemas.py
    ├── routers/
    │   ├── cats.py
    │   └── missions.py
    └── services/
        └── cat_breed_validator.py

---

## Setup & Installation

### 1. Clone the repository
    git clone https://github.com/st000ne/SpyCatAgencyBackend
    cd spy-cat-agency-backend

### 2. Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    venv\Scripts\activate   # Windows

### 3. Install dependencies
    pip install -r requirements.txt

---

## Running the Application

    uvicorn app.main:app --reload

The API will be available at:
http://localhost:8000

Interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Database

- The application uses SQLite
- Database file is created automatically on startup
- Tables are created automatically via SQLAlchemy metadata

---

## External API Usage

### TheCatAPI
- Used to validate cat breeds when creating spy cats
- Endpoint: https://api.thecatapi.com/v1/breeds
- In-memory caching is used to reduce external calls

---

## Notes & Limitations

- Authentication and authorization are intentionally omitted
- SQLite is used for simplicity
- In-memory caching is sufficient for this assessment scope

---

Developed as part of the Spy Cat Agency Python Full-Stack Engineer Test Assessment for DevelopsToday.
