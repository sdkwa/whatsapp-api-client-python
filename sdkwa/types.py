"""Type definitions for SDKWA API."""

from typing import Any, Dict, List, Optional, Union

try:
    from typing_extensions import TypedDict
except ImportError:
    from typing import TypedDict


# Common types
ChatId = str
MessageId = str
ReceiptId = int


class Contact(TypedDict, total=False):
    """Contact information."""
    phone_contact: int
    first_name: Optional[str]
    middle_name: Optional[str]  
    last_name: Optional[str]
    company: Optional[str]


class Location(TypedDict):
    """Location information."""
    name_location: Optional[str]
    address: Optional[str]
    latitude: float
    longitude: float


# Request types
class SendMessageRequest(TypedDict, total=False):
    """Send message request parameters."""
    chat_id: ChatId
    message: str
    quoted_message_id: Optional[MessageId]
    archive_chat: Optional[bool]
    link_preview: Optional[bool]


class SendContactRequest(TypedDict, total=False):
    """Send contact request parameters."""
    chat_id: ChatId
    contact: Contact
    quoted_message_id: Optional[MessageId]


class SendFileByUrlRequest(TypedDict, total=False):
    """Send file by URL request parameters."""
    chat_id: ChatId
    url_file: str
    file_name: str
    caption: Optional[str]
    quoted_message_id: Optional[MessageId]
    archive_chat: Optional[bool]


class SendLocationRequest(TypedDict, total=False):
    """Send location request parameters."""
    chat_id: ChatId
    name_location: Optional[str]
    address: Optional[str]
    latitude: float
    longitude: float
    quoted_message_id: Optional[MessageId]


class GetChatHistoryRequest(TypedDict, total=False):
    """Get chat history request parameters."""
    chat_id: ChatId
    count: Optional[int]


class DownloadFileRequest(TypedDict):
    """Download file request parameters."""
    chat_id: ChatId


class CreateGroupRequest(TypedDict):
    """Create group request parameters."""
    group_name: str
    chat_ids: List[ChatId]


class UpdateGroupNameRequest(TypedDict):
    """Update group name request parameters."""
    group_id: ChatId
    group_name: str


class AddGroupParticipantRequest(TypedDict):
    """Add group participant request parameters."""
    group_id: ChatId
    participant_chat_id: ChatId


class RemoveGroupParticipantRequest(TypedDict):
    """Remove group participant request parameters."""
    group_id: ChatId
    participant_chat_id: ChatId


class SetGroupAdminRequest(TypedDict):
    """Set group admin request parameters."""
    group_id: ChatId
    participant_chat_id: ChatId


class RemoveAdminRequest(TypedDict):
    """Remove admin request parameters."""
    group_id: ChatId
    participant_chat_id: ChatId


class GetAuthorizationCodeRequest(TypedDict):
    """Get authorization code request parameters."""
    phone_number: int


class SendRegistrationCodeRequest(TypedDict):
    """Send registration code request parameters."""
    code: str


class RequestRegistrationCodeRequest(TypedDict):
    """Request registration code parameters."""
    phone_number: int
    method: str  # "sms" or "voice"


# Response types
class SendMessageResponse(TypedDict):
    """Send message response."""
    id_message: MessageId


class SendContactResponse(TypedDict):
    """Send contact response."""
    id_message: MessageId


class SendFileResponse(TypedDict):
    """Send file response."""
    id_message: MessageId


class SendLocationResponse(TypedDict):
    """Send location response."""
    id_message: MessageId


class UploadFileResponse(TypedDict):
    """Upload file response."""
    url_file: str


class GetStateInstanceResponse(TypedDict):
    """Get state instance response."""
    state_instance: str


class SetSettingsResponse(TypedDict):
    """Set settings response."""
    save_settings: bool


class RebootResponse(TypedDict):
    """Reboot response."""
    is_reboot: bool


class LogoutResponse(TypedDict):
    """Logout response."""
    is_logout: bool


class QRCodeResponse(TypedDict):
    """QR code response."""
    type: str
    message: str


class GetAuthorizationCodeResponse(TypedDict):
    """Get authorization code response."""
    status: bool
    code: str


class DeleteNotificationResponse(TypedDict):
    """Delete notification response."""
    result: bool


class CreateGroupResponse(TypedDict):
    """Create group response."""
    chat_id: ChatId
    group_invite_link: str


class GetGroupDataResponse(TypedDict):
    """Get group data response."""
    group_name: str
    chat_id: ChatId
    owner: str
    creation: int
    participants: List[Dict[str, Any]]
    group_invite_link: str


# Notification types
class NotificationBody(TypedDict, total=False):
    """Base notification body."""
    type_webhook: str
    instance_data: Dict[str, Any]
    timestamp: int


class IncomingMessageNotification(NotificationBody):
    """Incoming message notification."""
    id_message: MessageId
    sender_data: Dict[str, Any]
    message_data: Dict[str, Any]


class OutgoingMessageStatusNotification(NotificationBody):
    """Outgoing message status notification."""
    id_message: MessageId
    status: str
    timestamp: int


class Notification(TypedDict):
    """Notification wrapper."""
    receipt_id: ReceiptId
    body: NotificationBody


# Settings types
class AccountSettings(TypedDict, total=False):
    """Account settings."""
    wid: Optional[str]
    country_instance: Optional[str]
    type_account: Optional[str]
    webhook_url: Optional[str]
    webhook_url_token: Optional[str]
    delay_send_messages_milliseconds: Optional[int]
    delay_send_messages_max_ms: Optional[int]
    mark_incoming_messages_readed: Optional[str]
    mark_incoming_messages_readed_on_reply: Optional[str]
    outgoing_webhook: Optional[str]
    outgoing_message_webhook: Optional[str]
    outgoing_api_message_webhook: Optional[str]
    state_webhook: Optional[str]
    incoming_webhook: Optional[str]
    device_webhook: Optional[str]
    status_instance_webhook: Optional[str]
    keep_online_status: Optional[str]
    proxy_instance: Optional[str]
    send_from_utc: Optional[str]
    send_to_utc: Optional[str]
