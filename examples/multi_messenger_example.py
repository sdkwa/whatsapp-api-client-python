#!/usr/bin/env python3
"""Example demonstrating multi-messenger support with per-request messenger selection."""

from sdkwa import SDKWA

# Example 1: Using default messenger (WhatsApp)
print("="*60)
print("Example 1: Default WhatsApp Client")
print("="*60)

# Create client with default WhatsApp messenger
whatsapp_client = SDKWA(
    id_instance="YOUR_WHATSAPP_INSTANCE_ID",
    api_token_instance="YOUR_WHATSAPP_TOKEN"
)

# All methods will use WhatsApp by default
# whatsapp_client.send_message("1234567890@c.us", "Hello via WhatsApp")
# whatsapp_client.get_contacts()
print(f"✓ Client created with default messenger: {whatsapp_client.default_messenger}")
print()

# Example 2: Single client, switching between messengers per request
print("="*60)
print("Example 2: Dynamic Messenger Selection (Per Request)")
print("="*60)

# Create a single client with WhatsApp as default
universal_client = SDKWA(
    id_instance="YOUR_INSTANCE_ID",
    api_token_instance="YOUR_TOKEN"
)

print(f"Default messenger: {universal_client.default_messenger}")
print()

# Send message via WhatsApp (using default)
print("Sending message via WhatsApp (default):")
# universal_client.send_message("1234567890@c.us", "Hello via WhatsApp")
print("  universal_client.send_message('1234567890@c.us', 'Hello via WhatsApp')")
print()

# Send message via Telegram (override messenger for this request)
print("Sending message via Telegram (override):")
# universal_client.send_message("1234567890", "Hello via Telegram", messenger="telegram")
print("  universal_client.send_message('1234567890', 'Hello via Telegram', messenger='telegram')")
print()

# Get WhatsApp contacts
print("Getting WhatsApp contacts (default):")
# whatsapp_contacts = universal_client.get_contacts()
print("  whatsapp_contacts = universal_client.get_contacts()")
print()

# Get Telegram contacts
print("Getting Telegram contacts (override):")
# telegram_contacts = universal_client.get_contacts(messenger="telegram")
print("  telegram_contacts = universal_client.get_contacts(messenger='telegram')")
print()


print()

# Example 3: Real-world use case - Broadcasting to both platforms
print("="*60)
print("Example 3: Broadcasting to Both Platforms")
print("="*60)

def broadcast_message(client, message):
    """Send the same message to both WhatsApp and Telegram."""
    print(f"Broadcasting: '{message}'")
    
    # Send to WhatsApp
    try:
        # client.send_message("whatsapp_chat_id@c.us", message, messenger="whatsapp")
        print("  ✓ Sent via WhatsApp")
    except Exception as e:
        print(f"  ✗ WhatsApp error: {e}")
    
    # Send to Telegram
    try:
        # client.send_message("telegram_chat_id", message, messenger="telegram")
        print("  ✓ Sent via Telegram")
    except Exception as e:
        print(f"  ✗ Telegram error: {e}")

# Use the universal client
broadcast_message(universal_client, "Important announcement!")
print()

print("="*60)
print("Summary")
print("="*60)
print("✓ The default messenger is always WhatsApp")
print("✓ You can override the messenger for any individual API call")
print("✓ All API methods support the optional 'messenger' parameter")
print("✓ This enables flexible multi-platform messaging workflows")
print("="*60)
