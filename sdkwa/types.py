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
    """Contact information.
    
    phoneContact is required according to the API spec.
    At least one of firstName, middleName, lastName, or company must be provided.
    """
    phoneContact: int  # Required
    firstName: Optional[str]
    middleName: Optional[str]  
    lastName: Optional[str]
    company: Optional[str]


class Location(TypedDict):
    """Location information."""
    nameLocation: Optional[str]
    address: Optional[str]
    latitude: float
    longitude: float


# Request types
class SendMessageRequest(TypedDict, total=False):
    """Send message request parameters."""
    chatId: ChatId
    message: str
    quotedMessageId: Optional[MessageId]
    archiveChat: Optional[bool]
    linkPreview: Optional[bool]


class SendContactRequest(TypedDict, total=False):
    """Send contact request parameters."""
    chatId: ChatId
    contact: Contact
    quotedMessageId: Optional[MessageId]


class SendFileByUrlRequest(TypedDict, total=False):
    """Send file by URL request parameters."""
    chatId: ChatId
    urlFile: str
    fileName: str
    caption: Optional[str]
    quotedMessageId: Optional[MessageId]
    archiveChat: Optional[bool]


class SendLocationRequest(TypedDict, total=False):
    """Send location request parameters."""
    chatId: ChatId
    nameLocation: Optional[str]
    address: Optional[str]
    latitude: float
    longitude: float
    quotedMessageId: Optional[MessageId]


class GetChatHistoryRequest(TypedDict, total=False):
    """Get chat history request parameters."""
    chatId: ChatId
    count: Optional[int]


class DownloadFileRequest(TypedDict):
    """Download file request parameters."""
    chatId: ChatId


class CreateGroupRequest(TypedDict):
    """Create group request parameters."""
    groupName: str
    chatIds: List[ChatId]


class UpdateGroupNameRequest(TypedDict):
    """Update group name request parameters."""
    groupId: ChatId
    groupName: str


class AddGroupParticipantRequest(TypedDict):
    """Add group participant request parameters."""
    groupId: ChatId
    participantChatId: ChatId


class RemoveGroupParticipantRequest(TypedDict):
    """Remove group participant request parameters."""
    groupId: ChatId
    participantChatId: ChatId


class SetGroupAdminRequest(TypedDict):
    """Set group admin request parameters."""
    groupId: ChatId
    participantChatId: ChatId


class RemoveAdminRequest(TypedDict):
    """Remove admin request parameters."""
    groupId: ChatId
    participantChatId: ChatId


class GetAuthorizationCodeRequest(TypedDict):
    """Get authorization code request parameters."""
    phoneNumber: int


class SendRegistrationCodeRequest(TypedDict):
    """Send registration code request parameters."""
    code: str


class RequestRegistrationCodeRequest(TypedDict):
    """Request registration code parameters."""
    phoneNumber: int
    method: str  # "sms" or "voice"


# Response types
class SendMessageResponse(TypedDict):
    """Send message response."""
    idMessage: MessageId


class SendContactResponse(TypedDict):
    """Send contact response."""
    idMessage: MessageId


class SendFileResponse(TypedDict):
    """Send file response."""
    idMessage: MessageId


class SendLocationResponse(TypedDict):
    """Send location response."""
    idMessage: MessageId


class UploadFileResponse(TypedDict):
    """Upload file response."""
    urlFile: str


class GetStateInstanceResponse(TypedDict):
    """Get state instance response."""
    stateInstance: str


class SetSettingsResponse(TypedDict):
    """Set settings response."""
    saveSettings: bool


class RebootResponse(TypedDict):
    """Reboot response."""
    isReboot: bool


class LogoutResponse(TypedDict):
    """Logout response."""
    isLogout: bool


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
    chatId: ChatId
    groupInviteLink: str


class GetGroupDataResponse(TypedDict):
    """Get group data response."""
    groupName: str
    chatId: ChatId
    owner: str
    creation: int
    participants: List[Dict[str, Any]]
    groupInviteLink: str


# Notification types
class NotificationBody(TypedDict, total=False):
    """Base notification body."""
    typeWebhook: str
    instanceData: Dict[str, Any]
    timestamp: int


class IncomingMessageNotification(NotificationBody):
    """Incoming message notification."""
    idMessage: MessageId
    senderData: Dict[str, Any]
    messageData: Dict[str, Any]


class OutgoingMessageStatusNotification(NotificationBody):
    """Outgoing message status notification."""
    idMessage: MessageId
    status: str
    timestamp: int


class Notification(TypedDict):
    """Notification wrapper."""
    receiptId: ReceiptId
    body: NotificationBody


# Settings types
class AccountSettings(TypedDict, total=False):
    """Account settings."""
    wid: Optional[str]
    countryInstance: Optional[str]
    typeAccount: Optional[str]
    webhookUrl: Optional[str]
    webhookUrlToken: Optional[str]
    delaySendMessagesMilliseconds: Optional[int]
    delaySendMessagesMaxMs: Optional[int]
    markIncomingMessagesReaded: Optional[str]
    markIncomingMessagesReadedOnReply: Optional[str]
    outgoingWebhook: Optional[str]
    outgoingMessageWebhook: Optional[str]
    outgoingAPIMessageWebhook: Optional[str]
    stateWebhook: Optional[str]
    incomingWebhook: Optional[str]
    deviceWebhook: Optional[str]
    statusInstanceWebhook: Optional[str]
    keepOnlineStatus: Optional[str]
    proxyInstance: Optional[str]
    sendFromUTC: Optional[str]
    sendToUTC: Optional[str]
