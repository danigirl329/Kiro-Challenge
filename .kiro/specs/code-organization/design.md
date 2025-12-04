# Code Organization Design

## Overview

Refactor the backend codebase into a clean, layered architecture with clear separation of concerns. The new structure will organize code by domain (events, users, registrations) with distinct layers for API handlers, business logic, and data access.

## Target Folder Structure

```
backend/
├── main.py                    # FastAPI app initialization and middleware
├── lambda_handler.py          # Lambda entry point
├── requirements.txt
├── docs/
│   └── index.html
├── api/                       # API layer (HTTP handlers)
│   ├── __init__.py
│   ├── events.py             # Event endpoints
│   ├── users.py              # User endpoints
│   └── registrations.py      # Registration endpoints
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── event_service.py      # Event business logic
│   ├── user_service.py       # User business logic
│   └── registration_service.py  # Registration business logic
├── repositories/              # Data access layer
│   ├── __init__.py
│   ├── event_repository.py   # Event database operations
│   ├── user_repository.py    # User database operations
│   └── registration_repository.py  # Registration database operations
├── models/                    # Data models (shared across layers)
│   ├── __init__.py
│   ├── event.py              # Event models
│   ├── user.py               # User models
│   └── registration.py       # Registration models
└── common/                    # Shared utilities
    ├── __init__.py
    └── exceptions.py         # Custom exceptions
```

## Layer Responsibilities

### API Layer (`api/`)
- Handle HTTP requests and responses
- Parse and validate request data
- Format response data
- Set HTTP status codes
- Handle CORS and middleware concerns
- Delegate to services for business logic

### Service Layer (`services/`)
- Implement business rules and workflows
- Coordinate between multiple repositories
- Handle complex operations (e.g., waitlist promotion)
- Validate business constraints
- Return domain objects or raise business exceptions

### Repository Layer (`repositories/`)
- Execute database queries
- Handle DynamoDB operations
- Convert between database format and domain models
- Manage database connections and tables
- Handle database-specific errors

### Models Layer (`models/`)
- Define Pydantic models for validation
- Shared across all layers
- No business logic or database code

## Migration Strategy

1. Create new folder structure
2. Extract models into domain-specific files
3. Create repository modules with existing database code
4. Create service modules with business logic
5. Create API router modules with handlers
6. Update main.py to use new routers
7. Remove old files (database.py, registration_db.py)
8. Test all endpoints

## Key Design Decisions

- **Domain-Driven**: Organize by domain (events, users, registrations) not by layer
- **Dependency Injection**: Services receive repository instances
- **Error Handling**: Use custom exceptions that map to HTTP status codes
- **Backward Compatibility**: Maintain all existing API contracts
