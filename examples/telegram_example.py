"""Example showcasing Telegram API features with SDKWA SDK."""

import os
from sdkwa import SDKWA
from sdkwa.exceptions import SDKWAError, ValidationError


def main():
    """Telegram API example."""
    print("🚀 SDKWA Telegram API - Example\n")
    
    # Initialize client for Telegram
    client = SDKWA(
        id_instance=os.getenv("SDKWA_ID_INSTANCE", "YOUR_INSTANCE_ID"),
        api_token_instance=os.getenv("SDKWA_API_TOKEN", "YOUR_API_TOKEN"),
        messenger="telegram"  # Set messenger to telegram
    )
    
    # Replace with actual chat ID
    telegram_chat_id = "1234567890"
    
    try:
        # 1. Account Management
        print("📱 Account Management")
        print("-" * 30)
        
        # Get account state
        state = client.get_state_instance()
        print(f"Account state: {state['stateInstance']}")
        
        # Get current settings
        settings = client.get_settings()
        print(f"Webhook URL: {settings.get('webhookUrl', 'Not set')}")
        
        # 2. Telegram Authorization
        print("\n🔐 Telegram Authorization")
        print("-" * 30)
        
        # Send confirmation code (if not already authorized)
        try:
            phone_number = 79001234567  # Replace with your phone number
            response = client.send_confirmation_code(phone_number=phone_number)
            print(f"✅ Confirmation code sent: {response['message']}")
            
            # Wait for user to receive the code, then sign in
            # Uncomment the following when you have the code:
            # confirmation_code = input("Enter confirmation code: ")
            # result = client.sign_in_with_confirmation_code(code=confirmation_code)
            # print(f"✅ Signed in: {result['message']}")
        except SDKWAError as e:
            print(f"ℹ️  Already authorized or error: {e}")
        
        # 3. Sending Messages
        print("\n📤 Sending Messages")
        print("-" * 30)
        
        # Send text message
        response = client.send_message(
            chat_id=telegram_chat_id,
            message="Hello from SDKWA Telegram SDK! 👋\n\nThis is a test message.",
            link_preview=True
        )
        print(f"✅ Text message sent: {response['idMessage']}")
        
        # Send file by URL
        file_response = client.send_file_by_url(
            chat_id=telegram_chat_id,
            url_file="https://picsum.photos/400/300",
            file_name="random_image.jpg",
            caption="Random image from Lorem Picsum 📸"
        )
        print(f"✅ File by URL sent: {file_response['idMessage']}")
        
        # Send location
        location_response = client.send_location(
            chat_id=telegram_chat_id,
            latitude=40.7128,
            longitude=-74.0060,
            name_location="New York City",
            address="New York, NY, USA"
        )
        print(f"✅ Location sent: {location_response['idMessage']}")
        
        # 4. Create Telegram App (Telegram Business feature)
        print("\n🎨 Telegram App Management")
        print("-" * 30)
        
        try:
            app = client.create_app(
                title="SDKWA Demo App",
                short_name="sdkwademo",
                url="https://sdkwa.pro",
                description="Demo application for SDKWA Telegram integration"
            )
            print(f"✅ App created with ID: {app['data']['appId']}")
        except SDKWAError as e:
            print(f"ℹ️  App creation error (may already exist): {e}")
        
        # 5. Message History
        print("\n📚 Message History")
        print("-" * 30)
        
        # Get chat history
        history = client.get_chat_history(
            chat_id=telegram_chat_id,
            count=5
        )
        print(f"Last {len(history)} messages retrieved")
        
        # Get recent messages
        outgoing = client.last_outgoing_messages(minutes=60)
        incoming = client.last_incoming_messages(minutes=60)
        print(f"Outgoing messages (last hour): {len(outgoing)}")
        print(f"Incoming messages (last hour): {len(incoming)}")
        
        # 6. Notifications
        print("\n🔔 Notification Handling")
        print("-" * 30)
        print("Checking for notifications (5 second timeout)...")
        
        notification = client.receive_notification()
        if notification:
            print(f"📨 Notification received: {notification['body']['typeWebhook']}")
            # Delete the notification after processing
            client.delete_notification(notification['receiptId'])
            print("✅ Notification processed and deleted")
        else:
            print("No notifications received")
        
        print("\n✅ Telegram example completed successfully!")
        print("\n💡 Tips:")
        print("   - Update chat_id with real Telegram chat ID")
        print("   - Make sure your instance is authorized for Telegram")
        print("   - Set up webhook URL for real-time notifications")
        print("   - Check the Telegram API docs for more features")
        
    except ValidationError as e:
        print(f"❌ Validation Error: {e}")
        print("Make sure you're using messenger='telegram' when initializing the client")
    except SDKWAError as e:
        print(f"❌ SDKWA API Error: {e}")
        if hasattr(e, 'status_code'):
            print(f"Status Code: {e.status_code}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    finally:
        # Clean up
        client.close()
        print("\n👋 Client closed. Example finished.")


if __name__ == "__main__":
    main()
