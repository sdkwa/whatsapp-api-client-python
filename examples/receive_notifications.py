"""Example: Receive notifications."""

import os
import time
from sdkwa import SDKWA


def main():
    """Receive notifications example."""
    # Initialize client
    client = SDKWA(
        id_instance=os.getenv("SDKWA_ID_INSTANCE", "YOUR_INSTANCE_ID"),
        api_token_instance=os.getenv("SDKWA_API_TOKEN", "YOUR_API_TOKEN"),
    )
    
    print("🔄 Starting notification listener...")
    print("Send a message to your WhatsApp to see notifications appear.")
    print("Press Ctrl+C to stop.\n")
    
    try:
        while True:
            try:
                # Try to receive a notification
                notification = client.receive_notification()
                
                if notification:
                    print(f"📨 New notification received!")
                    print(f"Receipt ID: {notification['receiptId']}")
                    
                    body = notification['body']
                    webhook_type = body.get('typeWebhook', 'unknown')
                    print(f"Type: {webhook_type}")
                    
                    # Handle different notification types
                    if webhook_type == 'incomingMessageReceived':
                        sender = body.get('senderData', {}).get('chatId', 'Unknown')
                        message_data = body.get('messageData', {})
                        message_type = message_data.get('typeMessage', 'unknown')
                        
                        print(f"📥 Incoming message from: {sender}")
                        print(f"Message type: {message_type}")
                        
                        if message_type == 'textMessage':
                            text = message_data.get('textMessageData', {}).get('textMessage', '')
                            print(f"Message: {text}")
                        
                    elif webhook_type == 'outgoingMessageStatus':
                        status = body.get('status', 'unknown')
                        print(f"📤 Outgoing message status: {status}")
                    
                    # Delete the notification after processing
                    delete_result = client.delete_notification(notification['receiptId'])
                    if delete_result.get('result'):
                        print("✅ Notification deleted from queue")
                    
                    print("-" * 50)
                
                else:
                    # No notification received, wait a bit
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n🛑 Stopping notification listener...")
                break
            except Exception as e:
                print(f"❌ Error receiving notification: {e}")
                time.sleep(5)  # Wait before retrying
                
    finally:
        client.close()
        print("👋 Notification listener stopped.")


if __name__ == "__main__":
    main()
