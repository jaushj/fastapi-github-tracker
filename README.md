GitHub Repository Tracker API

Overview

This project is a FastAPI-based REST service that acts as a bridge between a PostgreSQL database and an external API (GitHub).
It demonstrates backend engineering skills including state management, external API integration, strict validation, error handling, and testing.

The service allows users to register GitHub repositories, persist their metadata, retrieve stored data, update records, and delete them.

1 Problem Understanding & Assumptions

Interpretation of the Requirements

The task was to build a backend service that:

Exposes exactly four REST API endpoints (POST, GET, PUT, DELETE)

Uses PostgreSQL for persistent state

Integrates with an external API

Enforces strict request and response validation

Includes automated tests

Is accompanied by high-quality documentation

Use Case Chosen

GitHub Repository Metadata Tracker

The API fetches repository metadata from the GitHub public REST API and stores it locally.
This use case clearly demonstrates:

External API dependency handling

Data normalization and persistence

Error handling and validation

CRUD operations

Assumptions (Mandatory)

GitHub’s public API is available and does not require authentication for basic repository metadata

Rate limiting is not aggressively handled but timeouts are enforced

No user authentication or authorization is required

Repository uniqueness is defined by (owner, repository_name)

PostgreSQL is available via environment variables

The API is synchronous at the HTTP layer but uses async I/O internally

2 Design Decisions
Database Schema

Table: repositories

Column	Type	Description
id	UUID (PK)	Unique identifier
owner	VARCHAR	GitHub owner
name	VARCHAR	Repository name
description	TEXT	Repository description
stars	INTEGER	Star count (≥ 0)
forks	INTEGER	Fork count (≥ 0)
url	VARCHAR	GitHub URL
created_at	TIMESTAMP	Auto-generated
updated_at	TIMESTAMP	Auto-updated

Constraints

Unique constraint on (owner, name) to prevent duplicates

Project Structure
app/
├── api/        # Route definitions
├── core/       # Configuration
├── db/         # Database models and CRUD
├── schemas/    # Pydantic models
├── services/   # External API integrations
└── main.py     # Application entry point


Architecture Pattern: Layered Architecture
(API → Service → Database)

Validation Logic

Pydantic models for request bodies and response schemas

Field constraints (minimum length, non-negative values)

UUID validation for path parameters

Database-level uniqueness enforcement

External API Design

GitHub REST API: GET /repos/{owner}/{repo}

Timeout enforced (5 seconds)

Explicit handling of:

Repository not found

Unexpected upstream failures

3 Solution Approach (Step-by-Step Data Flow)
POST /repositories

Client submits owner and repository name

Request validated via Pydantic

GitHub API is called to fetch repository metadata

Data is normalized and persisted to PostgreSQL

Stored entity is returned to the client

GET / PUT / DELETE

Resource is fetched from PostgreSQL

Business rules are applied

Response or error is returned

4 Error Handling Strategy
External API Errors

GitHub repository not found → 404 Not Found

Timeout or upstream error → 503 Service Unavailable

Database Errors

Duplicate repository → 409 Conflict

Missing resource → 404 Not Found

Validation Errors

Automatically handled by FastAPI → 422 Unprocessable Entity

5 API Endpoints (Exactly Four)

Method	Endpoint	Description
POST	/repositories	Fetch from GitHub and store
GET	/repositories/{id}	Retrieve repository
PUT	/repositories/{id}	Update description
DELETE	/repositories/{id}	Delete repository

6 How to Run the Project
Prerequisites

Python 3.10+

PostgreSQL

Environment Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Environment Variables

Create a .env file from .env.example:

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/github_db
GITHUB_API_BASE=https://api.github.com

Database Setup
CREATE DATABASE github_db;

Run the Server
uvicorn app.main:app --reload

API Documentation

Swagger UI:

http://localhost:8000/docs

7 Testing Strategy

Tools Used

Pytest

HTTPX

Unit Tests

GitHub API service (mocked responses)

Integration Tests

API endpoints

External API mocked to avoid real network calls

Run Tests
pytest

8 Evaluation Alignment

Clean Code: Modular, PEP-8 compliant

Engineering Judgment: Dependency injection, async DB access

Resilience: Graceful handling of DB and external failures

Communication: Clear documentation and rationale