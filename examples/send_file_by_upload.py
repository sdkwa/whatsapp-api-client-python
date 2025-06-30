"""Example: Send a file by uploading it."""

import os
from sdkwa import SDKWA


def main():
    """Send a file by upload example."""
    # Initialize client
    client = SDKWA(
        id_instance=os.getenv("SDKWA_ID_INSTANCE", "YOUR_INSTANCE_ID"),
        api_token_instance=os.getenv("SDKWA_API_TOKEN", "YOUR_API_TOKEN"),
    )
    
    chat_id = "1234567890@c.us"  # Replace with actual chat ID
    file_path = "example_file.jpg"  # Replace with actual file path
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        print("Please create an example file or update the file_path variable.")
        return
    
    try:
        # Open and send the file
        with open(file_path, "rb") as file:
            response = client.send_file_by_upload(
                chat_id=chat_id,
                file=file,
                file_name=os.path.basename(file_path),
                caption="File uploaded via SDKWA Python SDK! 📁",
            )
        
        print(f"✅ File uploaded and sent successfully!")
        print(f"Message ID: {response['idMessage']}")
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
    
    finally:
        client.close()


if __name__ == "__main__":
    main()
