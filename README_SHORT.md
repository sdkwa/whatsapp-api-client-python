# SDKWA WhatsApp API - Python SDK

A modern, type-safe Python SDK for the SDKWA WhatsApp HTTP API.

## Quick Start

```python
from sdkwa import SDKWA

# Initialize client
client = SDKWA(
    id_instance="YOUR_INSTANCE_ID",
    api_token_instance="YOUR_API_TOKEN"
)

# Send a message
response = client.send_message(
    chat_id="1234567890@c.us",
    message="Hello from SDKWA! 👋"
)

print(f"Message sent with ID: {response['idMessage']}")
```

## Features

- ✅ Full API coverage
- ✅ Type-safe implementation
- ✅ Webhook support
- ✅ File handling (upload/download)
- ✅ Group management
- ✅ Message queues
- ✅ Comprehensive error handling

## Installation

```bash
pip install sdkwa-whatsapp-api-client
```

## Documentation

Visit our [documentation](https://docs.sdkwa.pro) for detailed guides and API reference.

## Support

- 📚 [Documentation](https://docs.sdkwa.pro)
- 💬 [Telegram Support](https://t.me/sdkwa_support)
- 🌐 [Official Website](https://sdkwa.pro)

## License

MIT License - see [LICENSE](LICENSE) file for details.
