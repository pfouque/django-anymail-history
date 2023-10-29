from __future__ import annotations

from anymail.message import AnymailMessage
from anymail.message import AnymailRecipientStatus
from anymail.message import AnymailStatus
from anymail.signals import AnymailTrackingEvent
from anymail.signals import EventType
from anymail.signals import post_send
from anymail.signals import tracking
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from anymail_history.models import MessageEvent
from anymail_history.models import SentMessage

# NOTE: https://anymail.dev/en/stable/tips/testing/#testing-your-app


@override_settings(EMAIL_BACKEND="anymail.backends.test.EmailBackend")
class TestPostSendStoreSentMessages(TestCase):
    def setUp(self):
        super().setUp()
        self.message = AnymailMessage(
            subject="Subject",
            body="Text Body",
            from_email="from@example.com",
            to=["to@example.com"],
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

    @override_settings(ANYMAIL_STORE_HTML=True)
    def test_store_html(self):
        assert SentMessage.objects.count() == 0

        post_send.send(
            sender=AnymailMessage,
            message=AnymailMessage(
                subject="Subject",
                body="Text Body",
                from_email="from@example.com",
                to=["to@example.com"],
                alternatives=[("<html></html>", "text/html")],
            ),
            status=self.build_anymail_status(
                {
                    "one@example.com": AnymailRecipientStatus("12345", "sent"),
                }
            ),
            esp_name="ESP_NAME",
        )
        assert SentMessage.objects.count() == 1
        sent_message = SentMessage.objects.first()
        assert sent_message.content_html == "<html></html>"

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
        assert MessageEvent.objects.count() == 0
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
        assert MessageEvent.objects.count() == 1

    def test_unknown_message(self):
        assert MessageEvent.objects.count() == 0
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
        assert MessageEvent.objects.count() == 0

    def test_multiple_messages(self):
        SentMessage.objects.create(
            esp_name="ESP_NAME",
            message_id="12345",
        )
        SentMessage.objects.create(
            esp_name="ESP_NAME",
            message_id="12345",
        )
        assert MessageEvent.objects.count() == 0
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
        assert MessageEvent.objects.count() == 2
