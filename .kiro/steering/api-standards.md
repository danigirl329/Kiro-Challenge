---
inclusion: fileMatch
fileMatchPattern: '**/*api*.py|**/*main*.py|**/*routes*.py|**/*endpoints*.py'
---

# REST API Standards and Conventions

This steering file defines the REST API standards and conventions to follow when working with API code in this project.

## HTTP Methods

Use HTTP methods according to their semantic meaning:

- **GET**: Retrieve resources (read-only, idempotent, cacheable)
- **POST**: Create new resources (non-idempotent)
- **PUT**: Update entire resources (idempotent)
- **PATCH**: Partial update of resources (idempotent)
- **DELETE**: Remove resources (idempotent)

## HTTP Status Codes

### Success Codes (2xx)
- **200 OK**: Successful GET, PUT, PATCH, or DELETE with response body
- **201 Created**: Successful POST that creates a resource
- **204 No Content**: Successful DELETE or update with no response body

### Client Error Codes (4xx)
- **400 Bad Request**: Invalid request syntax or validation error
- **401 Unauthorized**: Authentication required or failed
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource does not exist
- **409 Conflict**: Request conflicts with current state
- **422 Unprocessable Entity**: Validation error with detailed feedback

### Server Error Codes (5xx)
- **500 Internal Server Error**: Unexpected server error
- **502 Bad Gateway**: Invalid response from upstream server
- **503 Service Unavailable**: Server temporarily unavailable

## JSON Response Format Standards

### Success Response Format

```json
{
  "data": { ... },
  "metadata": {
    "timestamp": "2024-12-03T00:00:00Z",
    "version": "1.0.0"
  }
}
```

For single resources, return the object directly:
```json
{
  "id": "123",
  "name": "Resource Name",
  "status": "active"
}
```

For collections, return an array:
```json
[
  { "id": "1", "name": "Item 1" },
  { "id": "2", "name": "Item 2" }
]
```

### Error Response Format

All error responses must follow this structure:

```json
{
  "detail": "Human-readable error message",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format",
      "code": "INVALID_FORMAT"
    }
  ]
}
```

For simple errors:
```json
{
  "detail": "Resource not found"
}
```

### Validation Error Response (422)

```json
{
  "detail": "Validation error",
  "errors": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## API Endpoint Conventions

### URL Structure
- Use plural nouns for collections: `/events`, `/users`
- Use kebab-case for multi-word resources: `/event-registrations`
- Use path parameters for resource IDs: `/events/{event_id}`
- Use query parameters for filtering: `/events?status=active`

### Request/Response Headers
- **Content-Type**: `application/json` for JSON payloads
- **Accept**: `application/json` for JSON responses
- **Authorization**: `Bearer {token}` for authenticated requests

## Input Validation

- Validate all input data using Pydantic models
- Provide clear, actionable error messages
- Include field names in validation errors
- Validate data types, formats, and constraints
- Use appropriate field validators for complex validation

## Error Handling

- Catch and handle all exceptions gracefully
- Log errors with appropriate severity levels
- Never expose internal implementation details in error messages
- Return consistent error response format
- Use appropriate HTTP status codes

## CORS Configuration

When configuring CORS:
- Specify allowed origins explicitly (avoid `*` in production)
- Allow necessary HTTP methods
- Include required headers
- Set appropriate max-age for preflight caching

## Pagination (when applicable)

For large collections, implement pagination:

```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

Query parameters:
- `?page=1` - Page number (1-indexed)
- `?per_page=20` - Items per page
- `?limit=20&offset=0` - Alternative pagination style

## Filtering and Sorting

- Use query parameters for filtering: `?status=active&type=public`
- Use `sort` parameter for sorting: `?sort=created_at` or `?sort=-created_at` (descending)
- Support multiple sort fields: `?sort=status,-created_at`

## API Versioning

- Include version in URL path: `/v1/events`
- Or use Accept header: `Accept: application/vnd.api.v1+json`
- Maintain backward compatibility when possible

## Documentation

- Document all endpoints with clear descriptions
- Include request/response examples
- Document all query parameters and path parameters
- Specify required vs optional fields
- Include authentication requirements
