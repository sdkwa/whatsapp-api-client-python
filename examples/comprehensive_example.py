"""Comprehensive example showcasing all SDKWA API features."""

import os
import time
from sdkwa import SDKWA
from sdkwa.exceptions import SDKWAError


def main():
    """Comprehensive example of SDKWA Python SDK usage."""
    print("🚀 SDKWA WhatsApp API - Comprehensive Example\n")
    
    # Initialize client
    client = SDKWA(
        id_instance=os.getenv("SDKWA_ID_INSTANCE", "YOUR_INSTANCE_ID"),
        api_token_instance=os.getenv("SDKWA_API_TOKEN", "YOUR_API_TOKEN"),
    )
    
    # Replace with actual chat IDs
    personal_chat_id = "1234567890@c.us"
    
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
        
        # 2. Sending Messages
        print("\n📤 Sending Messages")
        print("-" * 30)
        
        # Send text message
        response = client.send_message(
            chat_id=personal_chat_id,
            message="Hello from SDKWA Python SDK! 👋\n\nThis is a comprehensive test of all features.",
            link_preview=True
        )
        print(f"✅ Text message sent: {response['idMessage']}")
        
        # Send contact
        contact_response = client.send_contact(
            chat_id=personal_chat_id,
            contact={
                "phoneContact": 1234567890,
                "firstName": "John",
                "lastName": "Doe",
                "company": "SDKWA Demo"
            }
        )
        print(f"✅ Contact sent: {contact_response['idMessage']}")
        
        # Send location
        location_response = client.send_location(
            chat_id=personal_chat_id,
            latitude=40.7128,
            longitude=-74.0060,
            name_location="New York City",
            address="New York, NY, USA"
        )
        print(f"✅ Location sent: {location_response['idMessage']}")
        
        # Send file by URL
        file_response = client.send_file_by_url(
            chat_id=personal_chat_id,
            url_file="https://picsum.photos/400/300",
            file_name="random_image.jpg",
            caption="Random image from Lorem Picsum 📸"
        )
        print(f"✅ File by URL sent: {file_response['idMessage']}")
        
        # 3. Message Queues
        print("\n📋 Message Queues")
        print("-" * 30)
        
        # Show queue
        queue = client.show_messages_queue()
        print(f"Messages in queue: {len(queue)}")
        
        # 4. Message History
        print("\n📚 Message History")
        print("-" * 30)
        
        # Get chat history
        history = client.get_chat_history(
            chat_id=personal_chat_id,
            count=5
        )
        print(f"Last {len(history)} messages retrieved")
        
        # Get recent messages
        outgoing = client.last_outgoing_messages(minutes=60)
        incoming = client.last_incoming_messages(minutes=60)
        print(f"Outgoing messages (last hour): {len(outgoing)}")
        print(f"Incoming messages (last hour): {len(incoming)}")
        
        # 5. Group Management (Optional - uncomment if you want to test)
        """
        print("\n👥 Group Management")
        print("-" * 30)
        
        # Create group
        group_response = client.create_group(
            group_name="SDKWA Test Group",
            chat_ids=[personal_chat_id]  # Add your own chat ID
        )
        group_id = group_response['chatId']
        print(f"✅ Group created: {group_id}")
        
        # Send message to group
        group_msg = client.send_message(
            chat_id=group_id,
            message="Welcome to the SDKWA test group! 🎉"
        )
        print(f"✅ Group message sent: {group_msg['idMessage']}")
        
        # Get group info
        group_info = client.get_group_data(group_id)
        print(f"Group name: {group_info['groupName']}")
        print(f"Participants: {len(group_info['participants'])}")
        
        # Leave group (cleanup)
        client.leave_group(group_id)
        print("✅ Left the test group")
        """
        
        # 6. Notifications (Demo)
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
        
        print("\n✅ Comprehensive example completed successfully!")
        print("\n💡 Tips:")
        print("   - Update chat IDs with real values for full testing")
        print("   - Set up webhook URL in account settings for real-time notifications")
        print("   - Check the examples/ folder for more specific use cases")
        
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
