"""Example: Send a file by URL."""

import os
from sdkwa import SDKWA


def main():
    """Send a file by URL example."""
    # Initialize client
    client = SDKWA(
        id_instance=os.getenv("SDKWA_ID_INSTANCE", "YOUR_INSTANCE_ID"),
        api_token_instance=os.getenv("SDKWA_API_TOKEN", "YOUR_API_TOKEN"),
    )
    
    chat_id = "1234567890@c.us"  # Replace with actual chat ID
    
    # Example image URL
    file_url = "https://picsum.photos/800/600"
    file_name = "example_image.jpg"
    caption = "This is an example image sent via SDKWA Python SDK! 📸"
    
    try:
        # Send the file
        response = client.send_file_by_url(
            chat_id=chat_id,
            url_file=file_url,
            file_name=file_name,
            caption=caption,
        )
        
        print(f"✅ File sent successfully!")
        print(f"Message ID: {response['idMessage']}")
        
    except Exception as e:
        print(f"❌ Error sending file: {e}")
    
    finally:
        client.close()


if __name__ == "__main__":
    main()
