"""Main SDKWA client."""

import os
from typing import Any, BinaryIO, Dict, List, Optional, Union

import requests

from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    ValidationError,
)
from .webhook import WebhookHandler


class SDKWA:
    """Main SDKWA API client for WhatsApp and Telegram."""

    def __init__(
        self,
        id_instance: Optional[str] = None,
        api_token_instance: Optional[str] = None,
        api_host: Optional[str] = None,
        user_id: Optional[str] = None,
        user_token: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = False,
    ) -> None:
        """Initialize SDKWA client.
        
        Args:
            id_instance: Instance ID (can be set via SDKWA_ID_INSTANCE env var)
            api_token_instance: API token (can be set via SDKWA_API_TOKEN env var)
            api_host: API host URL (can be set via SDKWA_API_HOST env var, defaults to https://api.sdkwa.pro)
            user_id: User ID for additional authentication (can be set via SDKWA_USER_ID env var)
            user_token: User token for additional authentication (can be set via SDKWA_USER_TOKEN env var)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            
        Raises:
            ValueError: If required parameters are missing or invalid
        """
        # Get values from environment if not provided
        self.id_instance = id_instance or os.getenv("SDKWA_ID_INSTANCE")
        self.api_token_instance = api_token_instance or os.getenv("SDKWA_API_TOKEN")
        self.api_host = (
            api_host 
            or os.getenv("SDKWA_API_HOST") 
            or "https://api.sdkwa.pro"
        )
        self.default_messenger = "whatsapp"  # Default messenger is always WhatsApp
        self.user_id = user_id or os.getenv("SDKWA_USER_ID")
        self.user_token = user_token or os.getenv("SDKWA_USER_TOKEN")
        
        # Validate required parameters
        if not self.id_instance:
            raise ValueError(
                "id_instance is required. Set it directly or via SDKWA_ID_INSTANCE environment variable."
            )
        if not self.api_token_instance:
            raise ValueError(
                "api_token_instance is required. Set it directly or via SDKWA_API_TOKEN environment variable."
            )
        
        # Strip whitespace and trailing slashes
        self.id_instance = self.id_instance.strip()
        self.api_token_instance = self.api_token_instance.strip()
        self.api_host = self.api_host.strip().rstrip("/")
        
        if self.user_id:
            self.user_id = self.user_id.strip()
        if self.user_token:
            self.user_token = self.user_token.strip()
        
        # Validate non-empty values
        if not self.id_instance:
            raise ValueError("id_instance cannot be empty")
        if not self.api_token_instance:
            raise ValueError("api_token_instance cannot be empty")
        
        # Set up HTTP client
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        # Set up default headers
        self.headers = {
            "Authorization": f"Bearer {self.api_token_instance}",
            "Content-Type": "application/json",
            "User-Agent": "sdkwa-python/1.0.0",
        }
        
        # Add optional auth headers
        if self.user_id:
            self.headers["x-user-id"] = self.user_id
        if self.user_token:
            self.headers["x-user-token"] = self.user_token
        
        # Create session for connection pooling
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.verify = self.verify_ssl
        
        # Initialize webhook handler
        self.webhook_handler = WebhookHandler()

    def _build_url(self, path: str, messenger: Optional[str] = None) -> str:
        """Build full URL from path.
        
        Args:
            path: API endpoint path
            messenger: Messenger type ('whatsapp' or 'telegram'). If None, uses default_messenger
            
        Returns:
            Full API URL
        """
        messenger_type = messenger or self.default_messenger
        
        # Validate messenger type
        if messenger_type not in ("whatsapp", "telegram"):
            raise ValueError(
                f"Invalid messenger type '{messenger_type}'. Must be 'whatsapp' or 'telegram'."
            )
        
        if not path.startswith("/"):
            path = "/" + path
        
        base_path = f"/{messenger_type}/{self.id_instance}"
        return f"{self.api_host}{base_path}{path}"

    def _handle_response(self, response: requests.Response) -> Any:
        """Handle HTTP response and raise appropriate exceptions."""
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            self._handle_http_error(response, e)
        
        # Handle empty responses
        if not response.content:
            return None
            
        # Try to parse JSON
        try:
            return response.json()
        except ValueError:
            # Return raw content for binary responses
            return response.content

    def _handle_http_error(self, response: requests.Response, error: requests.HTTPError) -> None:
        """Handle HTTP errors and convert to appropriate exceptions."""
        status_code = response.status_code
        
        try:
            error_data = response.json()
            message = error_data.get("message", str(error))
        except ValueError:
            message = response.text or str(error)
        
        if status_code == 401:
            raise AuthenticationError(message, status_code)
        elif status_code == 400:
            raise ValidationError(message, status_code)
        elif status_code == 429:
            raise RateLimitError(message, status_code)
        else:
            raise APIError(message, status_code)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        messenger: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """Make HTTP request to API.
        
        Args:
            method: HTTP method
            path: API endpoint path
            params: Query parameters
            json_data: JSON request body
            data: Raw request body
            files: Files for multipart upload
            headers: Additional headers
            messenger: Messenger type ('whatsapp' or 'telegram'). If None, uses default_messenger
            **kwargs: Additional arguments for requests
            
        Returns:
            Response data
            
        Raises:
            NetworkError: On network issues
            AuthenticationError: On auth failures
            ValidationError: On validation errors
            APIError: On other API errors
        """
        url = self._build_url(path, messenger=messenger)
        
        # Merge headers
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)
        
        # Remove content-type for multipart uploads
        if files:
            request_headers.pop("Content-Type", None)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                data=data,
                files=files,
                headers=request_headers,
                timeout=self.timeout,
                **kwargs,
            )
            return self._handle_response(response)
        except requests.RequestException as e:
            raise NetworkError(f"Network error: {e}")

    # --- Account methods ---
    def get_settings(self, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Get current account settings."""
        return self._request("GET", "/getSettings", messenger=messenger)

    def set_settings(self, settings: Dict[str, Any], messenger: Optional[str] = None) -> Dict[str, bool]:
        """Set account settings."""
        return self._request("POST", "/setSettings", json_data=settings, messenger=messenger)

    def get_state_instance(self, messenger: Optional[str] = None) -> Dict[str, str]:
        """Get account authorization state."""
        return self._request("GET", "/getStateInstance", messenger=messenger)

    def get_warming_phone_status(self, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Get account warming status."""
        return self._request("GET", "/getWarmingPhoneStatus", messenger=messenger)

    def reboot(self, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Reboot the account."""
        return self._request("GET", "/reboot", messenger=messenger)

    def logout(self, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Logout the account."""
        return self._request("GET", "/logout", messenger=messenger)

    def get_qr(self, messenger: Optional[str] = None) -> Dict[str, str]:
        """Get QR code for account authorization."""
        return self._request("GET", "/qr", messenger=messenger)

    def get_authorization_code(self, phone_number: int, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Get authorization code for phone number linking."""
        return self._request("POST", "/getAuthorizationCode", json_data={"phoneNumber": phone_number}, messenger=messenger)

    def request_registration_code(self, phone_number: int, method: str = "sms", messenger: Optional[str] = None) -> Dict[str, Any]:
        """Request registration code via SMS or voice call."""
        return self._request("POST", "/requestRegistrationCode", json_data={"phoneNumber": phone_number, "method": method}, messenger=messenger)

    def send_registration_code(self, code: str, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Send registration code received via SMS or call."""
        return self._request("POST", "/sendRegistrationCode", json_data={"code": code}, messenger=messenger)

    # --- Sending methods ---
    def send_message(
        self,
        chat_id: str,
        message: str,
        quoted_message_id: Optional[str] = None,
        archive_chat: Optional[bool] = None,
        link_preview: Optional[bool] = None,
        messenger: Optional[str] = None,
    ) -> Dict[str, str]:
        """Send a text message."""
        request_data = {"chatId": chat_id, "message": message}
        
        if quoted_message_id:
            request_data["quotedMessageId"] = quoted_message_id
        if archive_chat is not None:
            request_data["archiveChat"] = archive_chat
        if link_preview is not None:
            request_data["linkPreview"] = link_preview
            
        return self._request("POST", "/sendMessage", json_data=request_data, messenger=messenger)

    def send_contact(
        self,
        chat_id: str,
        contact: Dict[str, Any],
        quoted_message_id: Optional[str] = None,
        messenger: Optional[str] = None,
    ) -> Dict[str, str]:
        """Send a contact card."""
        request_data = {"chatId": chat_id, "contact": contact}
        
        if quoted_message_id:
            request_data["quotedMessageId"] = quoted_message_id
            
        return self._request("POST", "/sendContact", json_data=request_data, messenger=messenger)

    def send_file_by_upload(
        self,
        chat_id: str,
        file: Union[BinaryIO, bytes],
        file_name: str,
        caption: Optional[str] = None,
        quoted_message_id: Optional[str] = None,
        messenger: Optional[str] = None,
    ) -> Dict[str, str]:
        """Send a file by uploading it."""
        files = {"file": (file_name, file)}
        data = {"chatId": chat_id, "fileName": file_name}
        
        if caption:
            data["caption"] = caption
        if quoted_message_id:
            data["quotedMessageId"] = quoted_message_id
            
        return self._request("POST", "/sendFileByUpload", data=data, files=files, messenger=messenger)

    def send_file_by_url(
        self,
        chat_id: str,
        url_file: str,
        file_name: str,
        caption: Optional[str] = None,
        quoted_message_id: Optional[str] = None,
        archive_chat: Optional[bool] = None,
        messenger: Optional[str] = None,
    ) -> Dict[str, str]:
        """Send a file by URL."""
        request_data = {"chatId": chat_id, "urlFile": url_file, "fileName": file_name}
        
        if caption:
            request_data["caption"] = caption
        if quoted_message_id:
            request_data["quotedMessageId"] = quoted_message_id
        if archive_chat is not None:
            request_data["archiveChat"] = archive_chat
            
        return self._request("POST", "/sendFileByUrl", json_data=request_data, messenger=messenger)

    def send_location(
        self,
        chat_id: str,
        latitude: float,
        longitude: float,
        name_location: Optional[str] = None,
        address: Optional[str] = None,
        quoted_message_id: Optional[str] = None,
        messenger: Optional[str] = None,
    ) -> Dict[str, str]:
        """Send a location."""
        request_data = {"chatId": chat_id, "latitude": latitude, "longitude": longitude}
        
        if name_location:
            request_data["nameLocation"] = name_location
        if address:
            request_data["address"] = address
        if quoted_message_id:
            request_data["quotedMessageId"] = quoted_message_id
            
        return self._request("POST", "/sendLocation", json_data=request_data, messenger=messenger)

    def upload_file(self, file: Union[BinaryIO, bytes], messenger: Optional[str] = None) -> Dict[str, str]:
        """Upload a file to storage for later sending."""
        return self._request(
            "POST",
            "/uploadFile",
            data=file,
            headers={"Content-Type": "application/octet-stream"},
            messenger=messenger,
        )

    def get_chat_history(self, chat_id: str, count: Optional[int] = None, messenger: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get chat message history."""
        request_data = {"chatId": chat_id}
        if count:
            request_data["count"] = count
        return self._request("POST", "/getChatHistory", json_data=request_data, messenger=messenger)

    def download_file(self, chat_id: str, id_message: str, messenger: Optional[str] = None) -> bytes:
        """Download a file from a message."""
        request_data = {"chatId": chat_id}
        return self._request("POST", f"/downloadFile/{id_message}", json_data=request_data, messenger=messenger)

    # --- Receiving methods ---
    def receive_notification(self, messenger: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Receive a single incoming notification."""
        response = self._request("GET", "/receiveNotification", messenger=messenger)
        return response if response else None

    def delete_notification(self, receipt_id: int, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Delete a processed notification from the queue."""
        return self._request("DELETE", f"/deleteNotification/{receipt_id}", messenger=messenger)

    # --- Contact methods ---
    def get_contacts(self, messenger: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get contacts list."""
        return self._request("GET", "/getContacts", messenger=messenger)

    def get_chats(self, messenger: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get chats list."""
        return self._request("GET", "/getChats", messenger=messenger)

    def get_contact_info(self, chat_id: str, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Get contact information."""
        return self._request("POST", "/getContactInfo", json_data={"chatId": chat_id}, messenger=messenger)

    def check_whatsapp(self, phone_number: int, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Check if phone number has WhatsApp."""
        return self._request("POST", "/checkWhatsapp", json_data={"phoneNumber": phone_number}, messenger=messenger)

    def get_avatar(self, chat_id: str, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Get contact/group avatar."""
        return self._request("POST", "/getAvatar", json_data={"chatId": chat_id}, messenger=messenger)

    # --- Profile methods ---
    def set_profile_picture(self, file: Union[BinaryIO, bytes], messenger: Optional[str] = None) -> Dict[str, Any]:
        """Set profile picture."""
        files = {"file": file}
        return self._request("POST", "/setProfilePicture", files=files, messenger=messenger)

    def set_profile_name(self, name: str, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Set profile name."""
        return self._request("POST", "/setProfileName", json_data={"name": name}, messenger=messenger)

    def set_profile_status(self, status: str, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Set profile status."""
        return self._request("POST", "/setProfileStatus", json_data={"status": status}, messenger=messenger)

    # --- Group methods ---
    def create_group(self, group_name: str, chat_ids: List[str], messenger: Optional[str] = None) -> Dict[str, Any]:
        """Create a new group chat."""
        return self._request("POST", "/createGroup", json_data={"groupName": group_name, "chatIds": chat_ids}, messenger=messenger)

    def update_group_name(self, group_id: str, group_name: str, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Update group name."""
        return self._request("POST", "/updateGroupName", json_data={"groupId": group_id, "groupName": group_name}, messenger=messenger)

    def get_group_data(self, group_id: str, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Get group chat information."""
        return self._request("POST", "/getGroupData", json_data={"groupId": group_id}, messenger=messenger)

    def add_group_participant(self, group_id: str, participant_chat_id: str, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Add participant to group."""
        return self._request("POST", "/addGroupParticipant", json_data={"groupId": group_id, "participantChatId": participant_chat_id}, messenger=messenger)

    def remove_group_participant(self, group_id: str, participant_chat_id: str, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Remove participant from group."""
        return self._request("POST", "/removeGroupParticipant", json_data={"groupId": group_id, "participantChatId": participant_chat_id}, messenger=messenger)

    def set_group_admin(self, group_id: str, participant_chat_id: str, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Set participant as group admin."""
        return self._request("POST", "/setGroupAdmin", json_data={"groupId": group_id, "participantChatId": participant_chat_id}, messenger=messenger)

    def remove_admin(self, group_id: str, participant_chat_id: str, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Remove admin rights from participant."""
        return self._request("POST", "/removeAdmin", json_data={"groupId": group_id, "participantChatId": participant_chat_id}, messenger=messenger)

    def leave_group(self, group_id: str, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Leave a group chat."""
        return self._request("POST", "/leaveGroup", json_data={"groupId": group_id}, messenger=messenger)

    def set_group_picture(self, group_id: str, file: Union[BinaryIO, bytes], messenger: Optional[str] = None) -> Dict[str, Any]:
        """Set group picture."""
        files = {"file": file}
        data = {"groupId": group_id}
        return self._request("POST", "/setGroupPicture", data=data, files=files, messenger=messenger)

    # --- Read mark ---
    def read_chat(self, chat_id: str, id_message: Optional[str] = None, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Mark chat messages as read."""
        request_data = {"chatId": chat_id}
        if id_message:
            request_data["idMessage"] = id_message
        return self._request("POST", "/readChat", json_data=request_data, messenger=messenger)

    # --- Archive/Unarchive ---
    def archive_chat(self, chat_id: str, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Archive a chat."""
        return self._request("POST", "/archiveChat", json_data={"chatId": chat_id}, messenger=messenger)

    def unarchive_chat(self, chat_id: str, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Unarchive a chat."""
        return self._request("POST", "/unarchiveChat", json_data={"chatId": chat_id}, messenger=messenger)

    # --- Message deletion ---
    def delete_message(self, chat_id: str, id_message: str, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Delete a message."""
        return self._request("POST", "/deleteMessage", json_data={"chatId": chat_id, "idMessage": id_message}, messenger=messenger)

    # --- Queue methods ---
    def clear_messages_queue(self, messenger: Optional[str] = None) -> Dict[str, bool]:
        """Clear all pending messages from the sending queue."""
        return self._request("GET", "/clearMessagesQueue", messenger=messenger)

    def show_messages_queue(self, messenger: Optional[str] = None) -> List[Dict[str, Any]]:
        """Show messages currently in the sending queue."""
        return self._request("GET", "/showMessagesQueue", messenger=messenger)

    # --- Journal methods ---
    def last_outgoing_messages(self, minutes: int = 1440, messenger: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get last outgoing messages."""
        params = {"minutes": minutes} if minutes != 1440 else None
        return self._request("GET", "/lastOutgoingMessages", params=params, messenger=messenger)

    def last_incoming_messages(self, minutes: int = 1440, messenger: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get last incoming messages."""
        params = {"minutes": minutes} if minutes != 1440 else None
        return self._request("GET", "/lastIncomingMessages", params=params, messenger=messenger)

    # --- Static instance management methods ---
    @staticmethod
    def get_instances(api_host: str, user_id: str, user_token: str) -> Dict[str, Any]:
        """Get list of instances for user."""
        if not user_id or not user_token:
            raise ValueError("user_id and user_token are required for get_instances")
        
        url = f"{api_host}/api/v1/instance/user/instances/list"
        headers = {
            "x-user-id": user_id,
            "x-user-token": user_token,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def create_instance(
        api_host: str, 
        user_id: str, 
        user_token: str, 
        tariff: str, 
        period: str, 
        payment_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new instance."""
        if not user_id or not user_token:
            raise ValueError("user_id and user_token are required for create_instance")
        
        url = f"{api_host}/api/v1/instance/user/instance/createByOrder"
        headers = {
            "x-user-id": user_id,
            "x-user-token": user_token,
            "Content-Type": "application/json"
        }
        
        body = {"tariff": tariff, "period": period}
        if payment_type:
            body["paymentType"] = payment_type
        
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def extend_instance(
        api_host: str,
        user_id: str,
        user_token: str,
        id_instance: int,
        tariff: str,
        period: str,
        payment_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Extend an existing instance."""
        if not user_id or not user_token:
            raise ValueError("user_id and user_token are required for extend_instance")
        
        url = f"{api_host}/api/v1/instance/user/instance/extendByOrder"
        headers = {
            "x-user-id": user_id,
            "x-user-token": user_token,
            "Content-Type": "application/json"
        }
        
        body = {"idInstance": id_instance, "tariff": tariff, "period": period}
        if payment_type:
            body["paymentType"] = payment_type
        
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def delete_instance(api_host: str, user_id: str, user_token: str, id_instance: int) -> Dict[str, Any]:
        """Delete an instance."""
        if not user_id or not user_token:
            raise ValueError("user_id and user_token are required for delete_instance")
        
        url = f"{api_host}/api/v1/instance/user/instance/delete"
        headers = {
            "x-user-id": user_id,
            "x-user-token": user_token,
            "Content-Type": "application/json"
        }
        
        body = {"idInstance": id_instance}
        
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def restore_instance(api_host: str, user_id: str, user_token: str, id_instance: int) -> Dict[str, Any]:
        """Restore an instance."""
        if not user_id or not user_token:
            raise ValueError("user_id and user_token are required for restore_instance")
        
        url = f"{api_host}/api/v1/instance/user/instance/restore"
        headers = {
            "x-user-id": user_id,
            "x-user-token": user_token,
            "Content-Type": "application/json"
        }
        
        body = {"idInstance": id_instance}
        
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()

    # Telegram-specific methods
    
    def create_app(
        self,
        title: str,
        short_name: str,
        url: str,
        description: str,
        messenger: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create Telegram application (typically used with messenger='telegram').
        
        Args:
            title: Application title
            short_name: Application short name
            url: Application URL
            description: Application description
            messenger: Messenger type ('whatsapp' or 'telegram'), uses default if not specified
            
        Returns:
            dict: Response containing the created app ID
        """
        request_data = {
            "title": title,
            "shortName": short_name,
            "url": url,
            "description": description
        }
        
        return self._request("POST", "/createApp", json_data=request_data, messenger=messenger)
    
    def send_confirmation_code(self, phone_number: int, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Send confirmation code for Telegram authorization (typically used with messenger='telegram').
        
        Args:
            phone_number: Phone number to send confirmation code to
            messenger: Messenger type ('whatsapp' or 'telegram'), uses default if not specified
            
        Returns:
            dict: Response indicating if code was sent
        """
        return self._request(
            "POST",
            "/sendConfirmationCode",
            json_data={"phoneNumber": phone_number},
            messenger=messenger
        )
    
    def sign_in_with_confirmation_code(self, code: str, messenger: Optional[str] = None) -> Dict[str, Any]:
        """Sign in with confirmation code for Telegram (typically used with messenger='telegram').
        
        Args:
            code: Confirmation code received via SMS or app
            messenger: Messenger type ('whatsapp' or 'telegram'), uses default if not specified
            
        Returns:
            dict: Response indicating if sign in was successful
        """
        return self._request(
            "POST",
            "/signInWithConfirmationCode",
            json_data={"code": code},
            messenger=messenger
        )
    
    def close(self) -> None:
        """Close the client and cleanup resources."""
        self.session.close()

    def __enter__(self) -> "SDKWA":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"SDKWA(id_instance='{self.id_instance}', api_host='{self.api_host}')"
