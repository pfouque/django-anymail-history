from __future__ import annotations

from typing import Any

from anymail.message import AnymailMessage
from anymail.message import AnymailStatus
from anymail.signals import AnymailTrackingEvent
from anymail.signals import post_send
from anymail.signals import tracking
from anymail.utils import get_anymail_setting
from django.db.models import Model
from django.dispatch import receiver

from .models import MessageEvent
from .models import SentMessage


@receiver(post_send)
def store_sent_emails(
    sender: type[Model],
    message: AnymailMessage,
    status: AnymailStatus,
    esp_name: str,
    **kwargs: dict[Any, Any],
) -> None:
    content_html = None
    if get_anymail_setting("STORE_HTML", default=False):
        for content, mimetype in message.alternatives:
            if mimetype == "text/html":
                content_html = content

    for email, recipient_status in status.recipients.items():
        if (
            get_anymail_setting("STORE_FAILED_SEND", default=False)
            or recipient_status.message_id is not None
        ):
            SentMessage.objects.create(
                esp_name=esp_name,
                # NOTE: message_id might be None if send failed
                message_id=recipient_status.message_id,
                status=recipient_status.status,
                subject=message.subject,
                recipient_email=email,
                content=message.body,
                content_html=content_html,
            )


@receiver(tracking)
def handle_email_webhook_tracking(
    sender: type[Model],
    event: AnymailTrackingEvent,
    esp_name: str,
    **kwargs: dict[Any, Any],
) -> None:
    for sent_message in SentMessage.objects.exclude(message_id=None).filter(
        esp_name=esp_name, message_id=event.message_id
    ):
        MessageEvent.objects.create(
            sent_message=sent_message,
            created_on=event.timestamp,
            event_name=event.event_type,
            payload=event.esp_event,
        )
