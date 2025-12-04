# Implementation Plan

- [x] 1. Create new folder structure
  - Create api/, services/, repositories/, models/, common/ directories
  - Add __init__.py files to make them Python packages
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 2. Extract and organize models
  - Split models.py into domain-specific files (event.py, user.py, registration.py)
  - Move files to models/ directory
  - Update imports in models/__init__.py
  - _Requirements: 3.2, 5.4_

- [ ] 3. Create repository modules
  - Extract event database operations into repositories/event_repository.py
  - Extract user database operations into repositories/user_repository.py
  - Extract registration database operations into repositories/registration_repository.py
  - _Requirements: 2.1, 2.2, 2.5_

- [ ] 4. Create service modules
  - Create services/event_service.py with event business logic
  - Create services/user_service.py with user business logic
  - Create services/registration_service.py with registration and waitlist logic
  - _Requirements: 1.1, 1.3, 2.3_

- [ ] 5. Create API router modules
  - Create api/events.py with event endpoints
  - Create api/users.py with user endpoints
  - Create api/registrations.py with registration endpoints
  - _Requirements: 1.1, 1.2, 1.4, 1.5_

- [-] 6. Create custom exceptions
  - Create common/exceptions.py with business exceptions
  - Map exceptions to HTTP status codes
  - _Requirements: 4.4, 5.3_

- [ ] 7. Update main.py
  - Remove endpoint definitions
  - Import and include API routers
  - Keep middleware and app configuration
  - _Requirements: 1.5, 4.1, 4.2_

- [ ] 8. Clean up old files
  - Remove database.py
  - Remove registration_db.py
  - Remove old models.py
  - _Requirements: 2.4, 3.4_

- [ ] 9. Test all endpoints
  - Verify all existing endpoints work
  - Test error responses
  - Ensure backward compatibility
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_
