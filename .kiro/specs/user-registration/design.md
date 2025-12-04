# User Registration Feature Design

## Overview

The user registration system extends the existing Events API to support user management and event registration with capacity constraints and waitlist functionality. The system will allow users to register for events, manage their registrations, and automatically handle waitlist processing when spots become available.

## Architecture

The system follows a layered architecture pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                     API Layer (FastAPI)                      │
│  - User endpoints                                            │
│  - Registration endpoints                                    │
│  - Event registration queries                                │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
│  - Registration validation                                   │
│  - Capacity checking                                         │
│  - Waitlist management                                       │
│  - Automatic waitlist promotion                              │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Data Access Layer                         │
│  - User operations                                           │
│  - Registration operations                                   │
│  - Event operations (extended)                               │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      DynamoDB Tables                         │
│  - Users table                                               │
│  - Registrations table                                       │
│  - Events table (existing, extended)                         │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Data Models

#### User Model
```python
class User:
    userId: str          # Unique identifier (UUID or custom)
    name: str           # User's full name (1-200 chars)
    createdAt: str      # ISO 8601 timestamp
    updatedAt: str      # ISO 8601 timestamp
```

#### Extended Event Model
```python
class Event:
    # Existing fields...
    eventId: str
    title: str
    description: str
    date: str
    location: str
    organizer: str
    status: str
    
    # New fields for registration
    capacity: int                    # Maximum number of registrations
    hasWaitlist: bool               # Whether waitlist is enabled
    currentRegistrations: int       # Current count of registered users
    currentWaitlist: int           # Current count of waitlisted users
```

#### Registration Model
```python
class Registration:
    registrationId: str      # Unique identifier (composite: userId#eventId)
    userId: str             # Reference to User
    eventId: str            # Reference to Event
    status: str             # "registered" or "waitlisted"
    registeredAt: str       # ISO 8601 timestamp
    position: int           # Position in waitlist (null if registered)
```

### 2. API Endpoints

#### User Management
- `POST /users` - Create a new user
- `GET /users/{userId}` - Get user details
- `GET /users` - List all users
- `PUT /users/{userId}` - Update user information
- `DELETE /users/{userId}` - Delete a user

#### Registration Management
- `POST /events/{eventId}/register` - Register user for event
  - Request body: `{ "userId": "string" }`
  - Returns: Registration object with status
- `DELETE /events/{eventId}/register/{userId}` - Unregister user from event
- `GET /users/{userId}/registrations` - Get user's registrations
- `GET /events/{eventId}/registrations` - Get event's registrations and waitlist

### 3. Database Schema

#### Users Table
- **Partition Key**: `userId`
- **Attributes**: name, createdAt, updatedAt

#### Registrations Table
- **Partition Key**: `eventId`
- **Sort Key**: `userId`
- **GSI**: `userId-index` (for querying user's registrations)
- **Attributes**: registrationId, status, registeredAt, position

#### Events Table (Extended)
- **Partition Key**: `eventId`
- **New Attributes**: capacity, hasWaitlist, currentRegistrations, currentWaitlist

## Data Models

### Pydantic Models for Validation

```python
# User models
class UserCreate(BaseModel):
    userId: Optional[str] = None  # Auto-generated if not provided
    name: str = Field(..., min_length=1, max_length=200)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)

# Event models (extended)
class EventCreate(BaseModel):
    # ... existing fields ...
    capacity: int = Field(..., gt=0, le=100000)
    hasWaitlist: bool = Field(default=False)

# Registration models
class RegistrationRequest(BaseModel):
    userId: str = Field(..., min_length=1)

class RegistrationResponse(BaseModel):
    registrationId: str
    userId: str
    eventId: str
    status: str  # "registered" or "waitlisted"
    registeredAt: str
    position: Optional[int] = None
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: User creation uniqueness
*For any* userId, creating a user with that userId should succeed only if no user with that userId already exists
**Validates: Requirements 1.3**

### Property 2: Event capacity enforcement
*For any* event at full capacity without a waitlist, attempting to register a new user should be rejected
**Validates: Requirements 3.2**

### Property 3: Waitlist addition when full
*For any* event at full capacity with a waitlist enabled, registering a new user should add them to the waitlist with the correct position
**Validates: Requirements 3.3**

### Property 4: No duplicate registrations
*For any* user and event, if the user is already registered (either confirmed or waitlisted), attempting to register again should be rejected
**Validates: Requirements 3.4**

### Property 5: Waitlist promotion on unregister
*For any* event with a non-empty waitlist, when a registered user unregisters, the first user in the waitlist should be automatically promoted to registered status
**Validates: Requirements 4.2**

### Property 6: Registration count consistency
*For any* event, the currentRegistrations count should always equal the number of registrations with status "registered"
**Validates: Requirements 7.5**

### Property 7: Waitlist position consistency
*For any* event's waitlist, the positions should be sequential starting from 1 with no gaps
**Validates: Requirements 7.5**

### Property 8: Capacity constraint invariant
*For any* event, the number of confirmed registrations should never exceed the event's capacity
**Validates: Requirements 2.1, 3.1**

### Property 9: User deletion cascade
*For any* user, when deleted, all registrations and waitlist entries for that user should be removed
**Validates: Requirements 7.1**

### Property 10: Registration list completeness
*For any* user, querying their registrations should return all events they are registered for or waitlisted in
**Validates: Requirements 5.1, 5.2**

## Error Handling

### Error Scenarios and Responses

1. **User Not Found** (404)
   ```json
   {
     "detail": "User not found",
     "userId": "user-123"
   }
   ```

2. **Event Full** (409)
   ```json
   {
     "detail": "Event is at capacity and has no waitlist",
     "eventId": "event-456",
     "capacity": 100,
     "currentRegistrations": 100
   }
   ```

3. **Already Registered** (409)
   ```json
   {
     "detail": "User is already registered for this event",
     "userId": "user-123",
     "eventId": "event-456",
     "status": "registered"
   }
   ```

4. **Not Registered** (404)
   ```json
   {
     "detail": "User is not registered for this event",
     "userId": "user-123",
     "eventId": "event-456"
   }
   ```

5. **Duplicate User** (409)
   ```json
   {
     "detail": "User with this userId already exists",
     "userId": "user-123"
   }
   ```

### Error Handling Strategy

- Use appropriate HTTP status codes (400, 404, 409, 500)
- Provide detailed error messages with context
- Log all errors with appropriate severity
- Handle race conditions with optimistic locking or conditional updates
- Implement retry logic for transient failures
- Validate all inputs before processing

## Testing Strategy

### Unit Testing

Unit tests will verify individual functions and methods:

- User CRUD operations
- Registration validation logic
- Capacity checking functions
- Waitlist position calculation
- Automatic promotion logic

### Property-Based Testing

Property-based tests will verify universal properties using **Hypothesis** (Python property-based testing library):

- Each property test will run a minimum of 100 iterations
- Each test will be tagged with the format: `# Feature: user-registration, Property {number}: {property_text}`
- Tests will generate random users, events, and registration scenarios
- Tests will verify invariants hold across all generated inputs

**Property Test Examples:**

```python
# Feature: user-registration, Property 2: Event capacity enforcement
@given(event=events_at_capacity_without_waitlist(), user=users())
def test_capacity_enforcement(event, user):
    result = register_user(user.userId, event.eventId)
    assert result.status == "rejected"
    assert event.currentRegistrations == event.capacity

# Feature: user-registration, Property 5: Waitlist promotion on unregister
@given(event=events_with_waitlist(), registered_user=users(), waitlisted_users=lists(users(), min_size=1))
def test_waitlist_promotion(event, registered_user, waitlisted_users):
    # Setup: register user and add waitlist
    register_user(registered_user.userId, event.eventId)
    for user in waitlisted_users:
        register_user(user.userId, event.eventId)
    
    # Act: unregister
    unregister_user(registered_user.userId, event.eventId)
    
    # Assert: first waitlisted user is now registered
    first_waitlisted = waitlisted_users[0]
    registration = get_registration(first_waitlisted.userId, event.eventId)
    assert registration.status == "registered"
```

### Integration Testing

Integration tests will verify interactions between components:

- Complete registration flow (create user → register → verify)
- Waitlist promotion flow (register → fill capacity → unregister → verify promotion)
- User deletion cascade (create registrations → delete user → verify cleanup)
- Concurrent registration handling (multiple simultaneous registrations for last spot)

## Implementation Notes

### Concurrency Handling

To handle race conditions when multiple users register for the last available spot:

1. Use DynamoDB conditional updates with `currentRegistrations` as condition
2. Implement optimistic locking with version numbers
3. Retry failed registrations with exponential backoff
4. Return appropriate error if spot is taken during retry

### Waitlist Management

Waitlist positions should be managed efficiently:

1. Store position as an attribute in the Registration record
2. When promoting from waitlist, update positions for remaining waitlisted users
3. Use batch operations for position updates to minimize API calls
4. Consider using DynamoDB transactions for atomic waitlist operations

### Performance Considerations

- Use GSI for efficient querying of user registrations
- Implement pagination for large registration lists
- Cache event capacity and registration counts
- Use batch operations for bulk updates
- Consider using DynamoDB Streams for async processing

### Data Consistency

- Use DynamoDB transactions for operations that modify multiple items
- Implement idempotency keys for registration operations
- Validate data consistency in background jobs
- Monitor for drift between counts and actual registrations
