"""Custom exceptions for SDKWA API."""


class SDKWAError(Exception):
    """Base exception for SDKWA API errors."""
    
    def __init__(self, message: str, status_code: int = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(SDKWAError):
    """Raised when authentication fails."""
    pass


class ValidationError(SDKWAError):
    """Raised when request validation fails."""
    pass


class RateLimitError(SDKWAError):
    """Raised when rate limit is exceeded."""
    pass


class APIError(SDKWAError):
    """Raised when API returns an error response."""
    pass


class NetworkError(SDKWAError):
    """Raised when network request fails."""
    pass
