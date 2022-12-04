from __future__ import annotations

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from anymail.message import AnymailMessage, AnymailRecipientStatus, AnymailStatus
from anymail.signals import AnymailTrackingEvent, EventType, post_send, tracking

from anymail_history.models import SentMessage, SentMessageEvent


@override_settings(EMAIL_BACKEND="anymail.backends.test.EmailBackend")
class TestPostSendStoreSentMessages(TestCase):
    def setUp(self):
        super().setUp()
        self.message = AnymailMessage(
            "Subject", "Text Body", "from@example.com", ["to@example.com"]
        )

    @staticmethod
    def build_anymail_status(recipients):
        anymail_status = AnymailStatus()
        anymail_status.set_recipient_status(recipients)
        return anymail_status

    def test_single_recipient(self):
        recipients = {
            "one@example.com": AnymailRecipientStatus("12345", "sent"),
        }

        assert SentMessage.objects.count() == 0
        post_send.send(
            sender=AnymailMessage,
            message=self.message,
            status=self.build_anymail_status(recipients),
            esp_name="ESP_NAME",
        )
        assert SentMessage.objects.count() == 1
        sent_message = SentMessage.objects.first()
        assert sent_message.esp_name == "ESP_NAME"
        assert sent_message.message_id == "12345"
        assert sent_message.subject == "Subject"
        assert sent_message.content == "Text Body"
        assert sent_message.recipient_email == "one@example.com"
        assert sent_message.content_html is None

    def test_multiple_recipients(self):
        recipients = {
            "one@example.com": AnymailRecipientStatus("12345", "sent"),
            "two@example.com": AnymailRecipientStatus("45678", "queued"),
        }

        assert SentMessage.objects.count() == 0
        post_send.send(
            sender=AnymailMessage,
            message=self.message,
            status=self.build_anymail_status(recipients),
            esp_name="ESP_NAME",
        )
        assert SentMessage.objects.count() == 2

    def test_message_id_none(self):
        recipients = {
            "one@example.com": AnymailRecipientStatus(None, "sent"),
        }

        assert SentMessage.objects.count() == 0

        post_send.send(
            sender=AnymailMessage,
            message=self.message,
            status=self.build_anymail_status(recipients),
            esp_name="ESP_NAME",
        )
        assert SentMessage.objects.count() == 0

        with override_settings(ANYMAIL_STORE_FAILED_SEND=False):
            post_send.send(
                sender=AnymailMessage,
                message=self.message,
                status=self.build_anymail_status(recipients),
                esp_name="ESP_NAME",
            )
            assert SentMessage.objects.count() == 0

        with override_settings(ANYMAIL_STORE_FAILED_SEND=True):
            post_send.send(
                sender=AnymailMessage,
                message=self.message,
                status=self.build_anymail_status(recipients),
                esp_name="ESP_NAME",
            )
            assert SentMessage.objects.count() == 1

    def test_multiple_recipients_same_message_id(self):
        # status.message_id collapses when it's the same for all recipients
        recipients = {
            "one@example.com": AnymailRecipientStatus("12345", "sent"),
            "two@example.com": AnymailRecipientStatus("12345", "queued"),
        }

        assert SentMessage.objects.count() == 0
        post_send.send(
            sender=AnymailMessage,
            message=self.message,
            status=self.build_anymail_status(recipients),
            esp_name="ESP_NAME",
        )
        assert SentMessage.objects.count() == 2


@override_settings(EMAIL_BACKEND="anymail.backends.test.EmailBackend")
class TesttrackingisStored(TestCase):
    def test_message_exists(self):
        SentMessage.objects.create(
            esp_name="ESP_NAME",
            message_id="12345",
        )
        assert SentMessageEvent.objects.count() == 0
        tracking.send(
            sender=AnymailMessage,
            event=AnymailTrackingEvent(
                event_type=EventType.SENT,
                message_id="12345",
                timestamp=timezone.now(),
                esp_event={},
            ),
            esp_name="ESP_NAME",
        )
        assert SentMessageEvent.objects.count() == 1

    def test_unknown_message(self):
        assert SentMessageEvent.objects.count() == 0
        tracking.send(
            sender=AnymailMessage,
            event=AnymailTrackingEvent(
                event_type=EventType.SENT,
                message_id="12345",
                timestamp=timezone.now(),
                esp_event={},
            ),
            esp_name="ESP_NAME",
        )
        assert SentMessageEvent.objects.count() == 0

    def test_multiple_messages(self):
        SentMessage.objects.create(
            esp_name="ESP_NAME",
            message_id="12345",
        )
        SentMessage.objects.create(
            esp_name="ESP_NAME",
            message_id="12345",
        )
        assert SentMessageEvent.objects.count() == 0
        tracking.send(
            sender=AnymailMessage,
            event=AnymailTrackingEvent(
                event_type=EventType.SENT,
                message_id="12345",
                timestamp=timezone.now(),
                esp_event={},
            ),
            esp_name="ESP_NAME",
        )
        assert SentMessageEvent.objects.count() == 2
