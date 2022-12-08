from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone


class SentMessage(models.Model):
    created_on = models.DateTimeField(default=timezone.now, editable=False)

    esp_name = models.CharField(max_length=256, editable=False)
    message_id = models.CharField(max_length=256, null=True, editable=False)
    subject = models.CharField(max_length=998, editable=False)  # NOTE: RFC 2822
    content = models.TextField(null=True, editable=False)
    content_html = models.TextField(null=True, editable=False)
    status = models.CharField(max_length=256, editable=False)  # NOTE: AnymailStatus
    recipient_email = models.EmailField(editable=False)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["created_on"]),
            models.Index(fields=["message_id"]),
            models.Index(fields=["recipient_email"]),
        ]


class MessageEvent(models.Model):
    created_on = models.DateTimeField(editable=False)

    sent_message = models.ForeignKey(
        SentMessage,
        on_delete=models.CASCADE,
        editable=False,
        related_name="message_events",
    )
    event_name = models.CharField(max_length=32, editable=False)
    payload = models.JSONField(editable=False, default=dict)

    class Meta:
        indexes = [
            models.Index(fields=["created_on"]),
            models.Index(fields=["event_name"]),
        ]
