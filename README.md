# FDE Customer Platform

A production-oriented FastAPI customer platform built as part of my Forward Deployment Engineer (FDE) learning journey.

The project focuses on building, testing, containerizing, and continuously integrating a backend application using modern engineering practices.

## Tech Stack

- Python 3.14
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Pytest
- Requests
- Tenacity
- Docker
- Docker Compose
- GitHub Actions

## Architecture

```text
Client
  |
  v
FastAPI Router
  |
  v
Service Layer
  |
  v
Repository Layer
  |
  v
PostgreSQL
```

### Responsibilities

**Router**
- Handles HTTP requests and responses
- Request validation
- HTTP status codes

**Service**
- Business logic
- Transaction boundaries
- Error handling

**Repository**
- Database operations
- CRUD operations

**Models**
- Database representation

**Schemas**
- API request and response contracts

## Current API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application information |
| GET | `/health` | Health check |
| GET | `/live` | Liveness check |
| GET | `/ready` | Readiness check |
| POST | `/customers` | Create customer |
| GET | `/customers` | Get all customers |
| GET | `/customers/{id}` | Get customer |
| PUT | `/customers/{id}` | Full customer update |
| PATCH | `/customers/{id}` | Partial customer update |
| DELETE | `/customers/{id}` | Delete customer |
| GET | `/external-check` | External service integration |

## Reliability Concepts

The project also demonstrates production-oriented concepts including:

- Request IDs
- Structured application logging
- Health checks
- Liveness checks
- Readiness checks
- Database connectivity checks
- External API timeouts
- Retry handling
- Exponential backoff
- Graceful dependency failure
- HTTP 503 handling

## Testing

Run the automated tests locally:

```powershell
pytest
```

Or:

```powershell
python -m pytest
```

## Running Locally

Create and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Configure the database connection through `.env`.

Example:

```text
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<database>
```

Do not commit `.env` or database credentials to GitHub.

Start the application:

```powershell
uvicorn main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## Docker

Build and start the application:

```powershell
docker compose up --build
```

The application is exposed on:

```text
http://localhost:8000
```

Stop the containers:

```powershell
docker compose down
```

The PostgreSQL data is stored using a Docker named volume.

## CI/CD

GitHub Actions is used for Continuous Integration.

The current CI workflow:

```text
Git Push
   |
   v
GitHub Actions
   |
   v
Checkout source
   |
   v
Setup Python
   |
   v
Install dependencies
   |
   v
Run pytest
   |
   v
Pass / Fail
```

## FDE Learning Journey

This repository is being developed as a hands-on FDE learning project.

The learning progression is:

```text
Python
   ↓
FastAPI
   ↓
Pydantic
   ↓
SQLAlchemy
   ↓
PostgreSQL
   ↓
API Architecture
   ↓
Testing
   ↓
Logging & Observability
   ↓
Docker
   ↓
Git & GitHub
   ↓
CI/CD
   ↓
Reliability Engineering
   ↓
External APIs
   ↓
Retries & Timeouts
   ↓
Production Systems
```

The learning approach is:

**Learn → Build → Break → Debug → Improve → Deploy**

## Future Roadmap

Planned areas include:

- Authentication and authorization
- API integration patterns
- Idempotency
- Circuit breakers
- Redis
- Kafka
- Async Python
- Performance testing
- Prometheus metrics
- OpenTelemetry
- Kubernetes
- Advanced CI/CD
- AI API integration
- Tool calling
- RAG
- Production AI agents

## Project Goal

The goal is not only to learn individual technologies, but to understand how a production system behaves across:

**Application → Database → External Dependencies → Containers → CI/CD → Observability → Reliability**

---

Built as part of an FDE hands-on learning journey.