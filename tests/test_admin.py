from __future__ import annotations

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from anymail.signals import EventType

from anymail_history.models import MessageEvent, SentMessage


class TestSentMessageAdmin(TestCase):
    staff_client: Client

    def setUp(self):
        super().setUp()

        self.sent_message = SentMessage.objects.create(
            esp_name="ESP_NAME",
            message_id="12345",
        )
        MessageEvent.objects.create(
            sent_message=self.sent_message,
            created_on=timezone.now(),
            event_name=EventType.SENT,
            payload={},
        )

        user, _created = User.objects.get_or_create(
            username="test_admin",
            defaults={
                "password": User.objects.make_random_password(),
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        self.staff_client = Client()
        self.staff_client.force_login(user)

    def test_changelist(self):
        resp = self.staff_client.get(
            reverse("admin:anymail_history_sentmessage_changelist"),
        )
        assert resp.status_code == 200
        assert b"<!DOCTYPE html" in resp.content

    def test_change(self):
        resp = self.staff_client.get(
            reverse(
                "admin:anymail_history_sentmessage_change", args=[self.sent_message.pk]
            ),
        )
        assert resp.status_code == 200
        assert b"<!DOCTYPE html" in resp.content
