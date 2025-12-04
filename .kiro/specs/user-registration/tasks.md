# Implementation Plan

- [x] 1. Set up data models and database schema
  - Create User, Registration, and extended Event Pydantic models
  - Add capacity and waitlist fields to Event model
  - _Requirements: 1.1, 1.2, 2.1, 2.2_

- [x] 2. Implement user management
  - Create user CRUD operations in database layer
  - Add user API endpoints (POST, GET, PUT, DELETE)
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ]* 2.1 Write property test for user creation
  - **Property 1: User creation uniqueness**
  - **Validates: Requirements 1.3**

- [x] 3. Implement registration core logic
  - Create registration validation function
  - Implement capacity checking logic
  - Add registration to database operations
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ]* 3.1 Write property test for capacity enforcement
  - **Property 2: Event capacity enforcement**
  - **Validates: Requirements 3.2**

- [ ]* 3.2 Write property test for no duplicate registrations
  - **Property 4: No duplicate registrations**
  - **Validates: Requirements 3.4**

- [x] 4. Implement waitlist functionality
  - Add waitlist addition logic when event is full
  - Implement waitlist position tracking
  - Create waitlist query operations
  - _Requirements: 3.3, 2.4_

- [ ]* 4.1 Write property test for waitlist addition
  - **Property 3: Waitlist addition when full**
  - **Validates: Requirements 3.3**

- [ ]* 4.2 Write property test for waitlist position consistency
  - **Property 7: Waitlist position consistency**
  - **Validates: Requirements 7.5**

- [x] 5. Implement unregistration with waitlist promotion
  - Create unregister operation
  - Implement automatic waitlist promotion logic
  - Handle empty waitlist scenario
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ]* 5.1 Write property test for waitlist promotion
  - **Property 5: Waitlist promotion on unregister**
  - **Validates: Requirements 4.2**

- [x] 6. Implement registration queries
  - Add endpoint to get user's registrations
  - Add endpoint to get event's registrations and waitlist
  - Implement filtering by status (registered/waitlisted)
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 6.1, 6.2, 6.3_

- [ ]* 6.1 Write property test for registration list completeness
  - **Property 10: Registration list completeness**
  - **Validates: Requirements 5.1, 5.2**

- [x] 7. Add registration API endpoints
  - POST /events/{eventId}/register
  - DELETE /events/{eventId}/register/{userId}
  - GET /users/{userId}/registrations
  - GET /events/{eventId}/registrations
  - _Requirements: 3.1, 3.2, 3.3, 4.1, 5.1, 6.1_

- [ ] 8. Implement data integrity and cleanup
  - Add cascade delete for user registrations
  - Add cascade delete for event registrations
  - Implement consistency checks
  - _Requirements: 7.1, 7.2, 7.5_

- [ ]* 8.1 Write property test for user deletion cascade
  - **Property 9: User deletion cascade**
  - **Validates: Requirements 7.1**

- [ ]* 8.2 Write property test for registration count consistency
  - **Property 6: Registration count consistency**
  - **Validates: Requirements 7.5**

- [ ]* 8.3 Write property test for capacity invariant
  - **Property 8: Capacity constraint invariant**
  - **Validates: Requirements 2.1, 3.1**

- [x] 9. Update infrastructure for new tables
  - Add Users DynamoDB table to CDK stack
  - Add Registrations DynamoDB table with GSI
  - Update Lambda permissions for new tables
  - _Requirements: All_

- [ ] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
