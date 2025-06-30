# SDKWA WhatsApp API - Python SDK

[![PyPI version](https://badge.fury.io/py/sdkwa-whatsapp-api.svg)](https://badge.fury.io/py/sdkwa-whatsapp-api)
[![Python](https://img.shields.io/pypi/pyversions/sdkwa-whatsapp-api.svg)](https://pypi.org/project/sdkwa-whatsapp-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python SDK for the SDKWA WhatsApp HTTP API. Send messages, files, and manage WhatsApp accounts programmatically.

## Features

- 🚀 **Simple & Modern**: Clean, type-safe API following Python best practices
- 📱 **Full API Coverage**: Support for all SDKWA WhatsApp API endpoints
- 🔒 **Type Safe**: Complete type hints for better development experience
- 🪝 **Webhook Support**: Built-in webhook handling for real-time notifications
- 📁 **File Handling**: Send files by URL or upload with automatic type detection
- 🔄 **Async Support**: Optional async/await support for better performance
- 📦 **Zero Config**: Works out of the box with minimal setup

## Installation

```bash
pip install sdkwa-whatsapp-api
```

## Quick Start

```python
from sdkwa import SDKWA

# Initialize the client
client = SDKWA(
    id_instance="YOUR_INSTANCE_ID",
    api_token_instance="YOUR_API_TOKEN"
)

# Send a text message
response = client.sending.send_message(
    chat_id="1234567890@c.us",
    message="Hello from SDKWA! 👋"
)
print(f"Message sent with ID: {response.id_message}")

# Send a file
response = client.sending.send_file_by_url(
    chat_id="1234567890@c.us",
    url_file="https://example.com/image.jpg",
    file_name="image.jpg",
    caption="Check out this image!"
)

# Get account state
state = client.account.get_state_instance()
print(f"Account state: {state.state_instance}")
```

## API Reference

### Account Management

```python
# Get account settings
settings = client.account.get_settings()

# Update settings
client.account.set_settings({
    "webhook_url": "https://your-webhook-url.com",
    "delay_send_messages_milliseconds": 1000
})

# Get QR code for authorization
qr_data = client.account.get_qr_code()

# Reboot instance
client.account.reboot()

# Logout
client.account.logout()
```

### Sending Messages

```python
# Text message
client.sending.send_message(
    chat_id="1234567890@c.us",
    message="Hello World!",
    quoted_message_id="optional_message_id",  # Reply to message
    link_preview=True  # Enable link previews
)

# Send contact
client.sending.send_contact(
    chat_id="1234567890@c.us",
    contact={
        "phone_contact": 1234567890,
        "first_name": "John",
        "last_name": "Doe",
        "company": "Example Corp"
    }
)

# Send location
client.sending.send_location(
    chat_id="1234567890@c.us",
    name_location="My Location",
    address="123 Main St",
    latitude=40.7128,
    longitude=-74.0060
)
```

### File Operations

```python
# Send file by URL
client.sending.send_file_by_url(
    chat_id="1234567890@c.us",
    url_file="https://example.com/document.pdf",
    file_name="document.pdf",
    caption="Important document"
)

# Upload and send file
with open("image.jpg", "rb") as file:
    client.sending.send_file_by_upload(
        chat_id="1234567890@c.us",
        file=file,
        file_name="image.jpg",
        caption="Photo from vacation"
    )

# Download received file
file_data = client.sending.download_file(
    chat_id="1234567890@c.us",
    id_message="MESSAGE_ID"
)
```

### Receiving Messages

```python
# Get notifications
notification = client.receiving.receive_notification()
if notification:
    print(f"New notification: {notification.body}")
    # Process notification...
    
    # Delete notification after processing
    client.receiving.delete_notification(notification.receipt_id)

# Get chat history
history = client.sending.get_chat_history(
    chat_id="1234567890@c.us",
    count=50
)
```

### Group Management

```python
# Create group
group = client.groups.create_group(
    group_name="My Group",
    chat_ids=["1234567890@c.us", "0987654321@c.us"]
)

# Add participants
client.groups.add_group_participant(
    group_id=group.chat_id,
    participant_chat_id="1111111111@c.us"
)

# Update group name
client.groups.update_group_name(
    group_id="GROUP_ID@g.us",
    group_name="New Group Name"
)

# Leave group
client.groups.leave_group("GROUP_ID@g.us")
```

## Webhook Handling

```python
from flask import Flask, request
from sdkwa.webhook import WebhookHandler, WebhookType

app = Flask(__name__)
webhook_handler = WebhookHandler()

# Register event handlers
@webhook_handler.on(WebhookType.INCOMING_MESSAGE_RECEIVED)
def handle_message(notification):
    sender = notification.sender_data.chat_id
    message = notification.message_data.text_message_data.text_message
    print(f"Received message from {sender}: {message}")

@webhook_handler.on(WebhookType.OUTGOING_MESSAGE_STATUS)
def handle_status(notification):
    print(f"Message status: {notification.status}")

@app.route('/webhook', methods=['POST'])
def webhook():
    webhook_handler.handle(request.json)
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Configuration

### Environment Variables

```bash
export SDKWA_ID_INSTANCE="your_instance_id"
export SDKWA_API_TOKEN="your_api_token"
export SDKWA_API_HOST="https://api.sdkwa.pro"  # Optional
```

### Constructor Options

```python
client = SDKWA(
    id_instance="your_instance_id",
    api_token_instance="your_api_token",
    api_host="https://api.sdkwa.pro",  # Optional, defaults to official API
    user_id="your_user_id",  # Optional, for additional authentication
    user_token="your_user_token",  # Optional, for additional authentication
    timeout=30,  # Request timeout in seconds
    verify_ssl=True  # SSL verification
)
```

## Error Handling

```python
from sdkwa.exceptions import SDKWAError, AuthenticationError, ValidationError

try:
    response = client.sending.send_message(
        chat_id="invalid_chat_id",
        message="Test message"
    )
except AuthenticationError:
    print("Invalid credentials")
except ValidationError as e:
    print(f"Validation error: {e}")
except SDKWAError as e:
    print(f"API error: {e}")
```

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/sdkwa/whatsapp-api-client-python.git
cd whatsapp-api-client-python

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Format code
black .
isort .

# Type checking
mypy sdkwa
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📚 [Documentation](https://docs.sdkwa.pro)
- 💬 [Telegram Support](https://t.me/sdkwa_support)
- 🌐 [Official Website](https://sdkwa.pro)
- 🐛 [Report Issues](https://github.com/sdkwa/whatsapp-api-client-python/issues)

## Changelog

### v1.0.0
- Initial release
- Full API coverage for SDKWA WhatsApp API
- Type-safe implementation
- Webhook support
- Comprehensive documentation and examples
