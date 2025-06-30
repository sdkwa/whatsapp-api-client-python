"""SDKWA WhatsApp API Python SDK."""

from .client import SDKWA
from .exceptions import (
    SDKWAError,
    AuthenticationError, 
    ValidationError,
    RateLimitError,
    APIError,
    NetworkError,
)
from .webhook import WebhookHandler, WebhookType

__version__ = "1.0.0"
__all__ = [
    "SDKWA",
    "WebhookHandler",
    "WebhookType",
    "SDKWAError",
    "AuthenticationError", 
    "ValidationError",
    "RateLimitError",
    "APIError", 
    "NetworkError",
]
