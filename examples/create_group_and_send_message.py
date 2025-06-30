"""Example: Create a group and send a message."""

import os
from sdkwa import SDKWA


def main():
    """Create a group and send a message example."""
    # Initialize client
    client = SDKWA(
        id_instance=os.getenv("SDKWA_ID_INSTANCE", "YOUR_INSTANCE_ID"),
        api_token_instance=os.getenv("SDKWA_API_TOKEN", "YOUR_API_TOKEN"),
    )
    
    # List of participants (replace with actual phone numbers)
    participants = [
        "1234567890@c.us",  # Replace with actual participant chat IDs
        "0987654321@c.us",
    ]
    
    group_name = "SDKWA Test Group"
    
    try:
        # Create the group
        print(f"🔄 Creating group '{group_name}'...")
        group_response = client.create_group(
            group_name=group_name,
            chat_ids=participants,
        )
        
        group_id = group_response['chatId']
        invite_link = group_response.get('groupInviteLink', 'N/A')
        
        print(f"✅ Group created successfully!")
        print(f"Group ID: {group_id}")
        print(f"Invite Link: {invite_link}")
        
        # Send a welcome message to the group
        welcome_message = f"Welcome to {group_name}! 🎉\nThis group was created using the SDKWA Python SDK."
        
        print(f"\n🔄 Sending welcome message...")
        message_response = client.send_message(
            chat_id=group_id,
            message=welcome_message,
        )
        
        print(f"✅ Welcome message sent!")
        print(f"Message ID: {message_response['idMessage']}")
        
        # Get group information
        print(f"\n🔄 Getting group information...")
        group_info = client.get_group_data(group_id)
        
        print(f"📋 Group Information:")
        print(f"Name: {group_info['groupName']}")
        print(f"Owner: {group_info['owner']}")
        print(f"Participants: {len(group_info['participants'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        client.close()


if __name__ == "__main__":
    main()
