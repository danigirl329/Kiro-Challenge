"""Custom business exceptions that map to HTTP status codes"""


class BusinessException(Exception):
    """Base exception for business logic errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(BusinessException):
    """Resource not found"""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class ConflictException(BusinessException):
    """Resource conflict (duplicate, capacity exceeded, etc.)"""
    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class ValidationException(BusinessException):
    """Business validation error"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)
