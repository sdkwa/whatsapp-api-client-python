"""Example: Send a text message."""

import os
from sdkwa import SDKWA


def main():
    """Send a text message example."""
    # Initialize client (you can also pass credentials directly)
    client = SDKWA(
        id_instance=os.getenv("SDKWA_ID_INSTANCE", "YOUR_INSTANCE_ID"),
        api_token_instance=os.getenv("SDKWA_API_TOKEN", "YOUR_API_TOKEN"),
    )
    
    # Chat ID for personal chat: phone_number@c.us (e.g., 1234567890@c.us)
    # Chat ID for group chat: group_id@g.us
    chat_id = "1234567890@c.us"  # Replace with actual chat ID
    message = "Hello from SDKWA Python SDK! 👋"
    
    try:
        # Send the message
        response = client.send_message(
            chat_id=chat_id,
            message=message,
            link_preview=True,  # Enable link previews
        )
        
        print(f"✅ Message sent successfully!")
        print(f"Message ID: {response['idMessage']}")
        
    except Exception as e:
        print(f"❌ Error sending message: {e}")
    
    finally:
        # Close the client
        client.close()


if __name__ == "__main__":
    main()
