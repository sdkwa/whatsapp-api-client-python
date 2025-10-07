# SDKWA Messenger API Client - Python SDK

[![PyPI version](https://badge.fury.io/py/sdkwa-whatsapp-api-client.svg)](https://badge.fury.io/py/sdkwa-whatsapp-api-client)
[![Python](https://img.shields.io/pypi/pyversions/sdkwa-whatsapp-api-client.svg)](https://pypi.org/project/sdkwa-whatsapp-api-client/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python SDK for the SDKWA Messenger HTTP API. Send messages, files, and manage WhatsApp and Telegram accounts programmatically.

## Features

- 🚀 **Simple & Modern**: Clean, type-safe API following Python best practices
- 📱 **Multi-Messenger Support**: Support for both WhatsApp and Telegram
- 📡 **Full API Coverage**: Support for all SDKWA API endpoints
- 🔒 **Type Safe**: Complete type hints for better development experience
- 🪝 **Webhook Support**: Built-in webhook handling for real-time notifications
- 📁 **File Handling**: Send files by URL or upload with automatic type detection
- 🔄 **Async Support**: Optional async/await support for better performance
- 📦 **Zero Config**: Works out of the box with minimal setup

## Installation

```bash
pip install sdkwa-whatsapp-api-client
```

## Quick Start

### Step 1: Authorize Your Account (Scan QR Code)

Before you can send or receive messages, you need to authorize your WhatsApp account by scanning a QR code:

```python
from sdkwa import SDKWA

# Initialize the client
client = SDKWA(
    id_instance="YOUR_INSTANCE_ID",
    api_token_instance="YOUR_API_TOKEN"
)

# Get QR code for authorization
qr_data = client.get_qr()
print(f"QR Code: {qr_data['message']}")  # Display this QR code
print(f"Scan this QR code with your WhatsApp mobile app")

# Check authorization state
state = client.get_state_instance()
print(f"Account state: {state['stateInstance']}")
# Wait until state is "authorized" before sending messages
```

### Step 2: Send and Receive Messages

Once your account is authorized (QR code is scanned), you can start sending messages:

```python
from sdkwa import SDKWA

# Initialize the client (WhatsApp is the default messenger)
client = SDKWA(
    id_instance="YOUR_INSTANCE_ID",
    api_token_instance="YOUR_API_TOKEN"
)

# Send a text message
response = client.send_message(
    chat_id="1234567890@c.us",
    message="Hello from SDKWA! 👋"
)
print(f"Message sent with ID: {response['idMessage']}")

# Send a file
response = client.send_file_by_url(
    chat_id="1234567890@c.us",
    url_file="https://example.com/image.jpg",
    file_name="image.jpg",
    caption="Check out this image!"
)

# Get account state
state = client.get_state_instance()
print(f"Account state: {state['stateInstance']}")
```

### Using Telegram

For Telegram, you need to authorize using a confirmation code instead of QR:

```python
from sdkwa import SDKWA

# Create client and use messenger parameter for Telegram calls
client = SDKWA(
    id_instance="YOUR_INSTANCE_ID",
    api_token_instance="YOUR_API_TOKEN"
)

# Step 1: Authorize with Telegram
# Send confirmation code to your phone number
client.send_confirmation_code(phone_number=1234567890, messenger="telegram")

# Step 2: Enter the code you received
client.sign_in_with_confirmation_code(code="YOUR_CODE", messenger="telegram")

# Step 3: Now you can send messages
response = client.send_message(
    chat_id="1234567890",
    message="Hello from SDKWA Telegram! 👋",
    messenger="telegram"
)

# Telegram-specific methods
app = client.create_app(
    title="My App",
    short_name="myapp",
    url="https://myapp.com",
    description="My awesome Telegram app",
    messenger="telegram"
)
```

## API Reference

### Account Management

```python
# Get account settings
settings = client.get_settings()

# Update settings
client.set_settings({
    "webhookUrl": "https://your-webhook-url.com",
    "delaySendMessagesMilliseconds": 1000
})

# Get QR code for authorization
qr_data = client.get_qr()

# Get account state
state = client.get_state_instance()
print(f"Account state: {state['stateInstance']}")

# Reboot instance
client.reboot()

# Logout
client.logout()
```

### Sending Messages

```python
# Text message
client.send_message(
    chat_id="1234567890@c.us",
    message="Hello World!",
    quoted_message_id="optional_message_id",  # Reply to message
    link_preview=True  # Enable link previews
)

# Send contact
client.send_contact(
    chat_id="1234567890@c.us",
    contact={
        "phoneContact": 1234567890,
        "firstName": "John",
        "lastName": "Doe",
        "company": "Example Corp"
    }
)

# Send location
client.send_location(
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
client.send_file_by_url(
    chat_id="1234567890@c.us",
    url_file="https://example.com/document.pdf",
    file_name="document.pdf",
    caption="Important document"
)

# Upload and send file
with open("image.jpg", "rb") as file:
    client.send_file_by_upload(
        chat_id="1234567890@c.us",
        file=file,
        file_name="image.jpg",
        caption="Photo from vacation"
    )

# Download received file
file_data = client.download_file(
    chat_id="1234567890@c.us",
    id_message="MESSAGE_ID"
)
```

### Receiving Messages

```python
# Get notifications
notification = client.receive_notification()
if notification:
    print(f"New notification: {notification}")
    # Process notification...
    
    # Delete notification after processing
    client.delete_notification(notification['receiptId'])

# Get chat history
history = client.get_chat_history(
    chat_id="1234567890@c.us",
    count=50
)
```

### Groups and Contacts

```python
# Create group
group = client.create_group(
    group_name="My Group",
    chat_ids=["1234567890@c.us", "0987654321@c.us"]
)

# Get group data
group_info = client.get_group_data("GROUP_ID@g.us")

# Add participants to group
client.add_group_participant(
    group_id="GROUP_ID@g.us",
    participant_chat_id="1111111111@c.us"
)

# Remove participant from group
client.remove_group_participant(
    group_id="GROUP_ID@g.us",
    participant_chat_id="1111111111@c.us"
)

# Set group admin
client.set_group_admin(
    group_id="GROUP_ID@g.us",
    participant_chat_id="1111111111@c.us"
)

# Remove admin rights
client.remove_admin(
    group_id="GROUP_ID@g.us",
    participant_chat_id="1111111111@c.us"
)

# Update group name
client.update_group_name(
    group_id="GROUP_ID@g.us",
    group_name="New Group Name"
)

# Set group picture
with open("group_pic.jpg", "rb") as file:
    client.set_group_picture("GROUP_ID@g.us", file)

# Leave group
client.leave_group("GROUP_ID@g.us")

# Get contacts
contacts = client.get_contacts()

# Get chats
chats = client.get_chats()

# Get contact info
contact_info = client.get_contact_info("1234567890@c.us")

# Check if number has WhatsApp
has_whatsapp = client.check_whatsapp(1234567890)

# Get avatar
avatar = client.get_avatar("1234567890@c.us")

# Set profile picture
with open("profile_pic.jpg", "rb") as file:
    client.set_profile_picture(file)
```

### Chat Management

```python
# Mark chat as read
client.read_chat("1234567890@c.us")

# Mark specific message as read
client.read_chat("1234567890@c.us", id_message="MESSAGE_ID")

# Archive chat
client.archive_chat("1234567890@c.us")

# Unarchive chat
client.unarchive_chat("1234567890@c.us")

# Delete message
client.delete_message("1234567890@c.us", "MESSAGE_ID")
```

### Queue Management

```python
# Show messages in queue
queue = client.show_messages_queue()

# Clear messages queue
client.clear_messages_queue()
```

### Message History

```python
# Get last outgoing messages (last 24 hours by default)
outgoing = client.last_outgoing_messages()

# Get last outgoing messages from last 60 minutes
outgoing = client.last_outgoing_messages(minutes=60)

# Get last incoming messages
incoming = client.last_incoming_messages()
```

## Webhook Handling

```python
from flask import Flask, request
from sdkwa import WebhookHandler, WebhookType

app = Flask(__name__)
webhook_handler = WebhookHandler()

# Register event handlers
@webhook_handler.on(WebhookType.INCOMING_MESSAGE_RECEIVED)
def handle_message(notification):
    """Handle incoming message notifications."""
    sender_data = notification.get('senderData', {})
    message_data = notification.get('messageData', {})
    
    sender = sender_data.get('chatId', 'Unknown')
    sender_name = sender_data.get('senderName', 'Unknown')
    message_type = message_data.get('typeMessage', 'unknown')
    
    print(f"📥 Incoming message from {sender_name} ({sender})")
    
    if message_type == 'textMessage':
        text = message_data.get('textMessageData', {}).get('textMessage', '')
        print(f"Message: {text}")

@webhook_handler.on(WebhookType.OUTGOING_MESSAGE_STATUS)
def handle_status(notification):
    """Handle outgoing message status notifications."""
    status = notification.get('status', 'unknown')
    id_message = notification.get('idMessage', '')
    print(f"📤 Message {id_message} status: {status}")

@app.route('/webhook', methods=['POST'])
def webhook():
    webhook_handler.handle(request.json)
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Telegram-Specific Methods

The SDK provides special methods for Telegram messenger:

### Create Telegram App

```python
# Create a Telegram Business app
app = client.create_app(
    title="My Business App",
    short_name="mybusiness",
    url="https://mybusiness.com",
    description="Official business application"
)
print(f"App created with ID: {app['data']['appId']}")
```

### Telegram Authorization

```python
# Send confirmation code to phone number
response = client.send_confirmation_code(phone_number=79001234567)
print(f"Confirmation code sent: {response['message']}")

# Sign in with the received code
result = client.sign_in_with_confirmation_code(code="JpkyJeAM8dQ")
print(f"Sign in successful: {result['message']}")
```

## Configuration

### Environment Variables

```bash
export SDKWA_ID_INSTANCE="your_instance_id"
export SDKWA_API_TOKEN="your_api_token"
export SDKWA_API_HOST="https://api.sdkwa.pro"  # Optional
export SDKWA_MESSENGER="whatsapp"  # Optional: 'whatsapp' or 'telegram', defaults to 'whatsapp'
```

### Constructor Options

```python
client = SDKWA(
    id_instance="your_instance_id",
    api_token_instance="your_api_token",
    api_host="https://api.sdkwa.pro",  # Optional, defaults to official API
    messenger="whatsapp",  # Optional: 'whatsapp' or 'telegram', defaults to 'whatsapp'
    user_id="your_user_id",  # Optional, for additional authentication
    user_token="your_user_token",  # Optional, for additional authentication
    timeout=30,  # Request timeout in seconds
    verify_ssl=True  # SSL verification
)
```

## Error Handling

```python
from sdkwa import APIError, AuthenticationError, ValidationError

try:
    response = client.send_message(
        chat_id="invalid_chat_id",
        message="Test message"
    )
except AuthenticationError:
    print("Invalid credentials")
except ValidationError as e:
    print(f"Validation error: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/sdkwa/whatsapp-api-client-python.git
cd whatsapp-api-client-python

# Install in development mode
pip install -e .

# Format code
python scripts/dev.py format

# Clean build artifacts
python scripts/dev.py clean

# Build package
python scripts/dev.py build

# Publish to PyPI (requires API token)
python scripts/dev.py publish
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
