"""Example: Webhook server using Flask."""

import os
from flask import Flask, request, jsonify
from sdkwa import WebhookHandler, WebhookType


app = Flask(__name__)
webhook_handler = WebhookHandler()


# Register webhook handlers
@webhook_handler.on(WebhookType.INCOMING_MESSAGE_RECEIVED)
def handle_incoming_message(notification):
    """Handle incoming message notifications."""
    sender_data = notification.get('senderData', {})
    message_data = notification.get('messageData', {})
    
    sender = sender_data.get('chatId', 'Unknown')
    sender_name = sender_data.get('senderName', 'Unknown')
    message_type = message_data.get('typeMessage', 'unknown')
    
    print(f"📥 Incoming message from {sender_name} ({sender})")
    print(f"Type: {message_type}")
    
    if message_type == 'textMessage':
        text = message_data.get('textMessageData', {}).get('textMessage', '')
        print(f"Message: {text}")
    
    # You can add your custom logic here
    # For example, auto-reply to certain messages


@webhook_handler.on(WebhookType.OUTGOING_MESSAGE_STATUS)
def handle_outgoing_status(notification):
    """Handle outgoing message status notifications."""
    status = notification.get('status', 'unknown')
    id_message = notification.get('idMessage', 'unknown')
    
    print(f"📤 Message {id_message} status: {status}")


@webhook_handler.on(WebhookType.STATE_INSTANCE_CHANGED)
def handle_state_change(notification):
    """Handle instance state change notifications."""
    state = notification.get('stateInstance', 'unknown')
    print(f"🔄 Instance state changed to: {state}")


@webhook_handler.on(WebhookType.DEVICE_INFO)
def handle_device_info(notification):
    """Handle device information notifications."""
    print(f"📱 Device info update: {notification}")


@app.route('/webhook', methods=['POST'])
def webhook_endpoint():
    """Webhook endpoint to receive notifications."""
    try:
        # Get the JSON data from the request
        notification_data = request.get_json()
        
        if not notification_data:
            return jsonify({"error": "No JSON data received"}), 400
        
        # Handle the notification
        webhook_handler.handle(notification_data)
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.route('/', methods=['GET'])
def index():
    """Index page with basic information."""
    return """
    <h1>SDKWA Webhook Server</h1>
    <p>This is a webhook server for SDKWA WhatsApp API notifications.</p>
    <ul>
        <li><strong>Webhook endpoint:</strong> POST /webhook</li>
        <li><strong>Health check:</strong> GET /health</li>
    </ul>
    <p>Configure your SDKWA instance to send webhooks to: <code>https://your-domain.com/webhook</code></p>
    """


def main():
    """Run the webhook server."""
    print("🚀 Starting SDKWA Webhook Server...")
    print("📝 Configure your SDKWA instance webhook URL to point to this server.")
    print("🌐 Example: https://your-domain.com/webhook")
    print("\n💡 To test locally with ngrok:")
    print("   1. Install ngrok: https://ngrok.com/")
    print("   2. Run: ngrok http 5000")
    print("   3. Use the ngrok URL as your webhook URL")
    print("\n🛑 Press Ctrl+C to stop the server\n")
    
    # Get configuration from environment
    host = os.getenv('WEBHOOK_HOST', '0.0.0.0')
    port = int(os.getenv('WEBHOOK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Run the Flask app
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
