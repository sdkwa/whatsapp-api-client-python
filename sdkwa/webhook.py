"""Webhook handling utilities."""

from enum import Enum
from typing import Any, Callable, Dict, Optional

from .types import NotificationBody


class WebhookType(Enum):
    """Webhook notification types."""
    
    INCOMING_MESSAGE_RECEIVED = "incomingMessageReceived"
    OUTGOING_MESSAGE_RECEIVED = "outgoingMessageReceived"
    OUTGOING_MESSAGE_STATUS = "outgoingMessageStatus"
    STATE_INSTANCE_CHANGED = "stateInstanceChanged"
    DEVICE_INFO = "deviceInfo"
    STATUS_INSTANCE_CHANGED = "statusInstanceChanged"


WebhookCallback = Callable[[NotificationBody], None]


class WebhookHandler:
    """Handles incoming webhook notifications."""

    def __init__(self) -> None:
        self._handlers: Dict[str, WebhookCallback] = {}

    def on(self, webhook_type: WebhookType) -> Callable[[WebhookCallback], WebhookCallback]:
        """Decorator to register webhook handler.
        
        Args:
            webhook_type: Type of webhook to handle
            
        Returns:
            Decorator function
        """
        def decorator(func: WebhookCallback) -> WebhookCallback:
            self._handlers[webhook_type.value] = func
            return func
        return decorator

    def register(self, webhook_type: WebhookType, callback: WebhookCallback) -> None:
        """Register a webhook handler.
        
        Args:
            webhook_type: Type of webhook to handle
            callback: Callback function to handle the webhook
        """
        self._handlers[webhook_type.value] = callback

    def handle(self, notification: Dict[str, Any]) -> None:
        """Handle incoming webhook notification.
        
        Args:
            notification: Webhook notification data
        """
        if not notification or "body" not in notification:
            return
            
        body = notification["body"]
        webhook_type = body.get("typeWebhook")
        
        if webhook_type and webhook_type in self._handlers:
            self._handlers[webhook_type](body)

    def remove_handler(self, webhook_type: WebhookType) -> None:
        """Remove a webhook handler.
        
        Args:
            webhook_type: Type of webhook handler to remove
        """
        self._handlers.pop(webhook_type.value, None)
