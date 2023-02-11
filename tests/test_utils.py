from __future__ import annotations

from unittest.mock import Mock
from unittest.mock import patch

from anymail.exceptions import AnymailAPIError
from django.test import TestCase

from anymail_history import HtmlAnymailMessage
from anymail_history import send_templated_email


@patch("anymail.message.AnymailMessage.send")
@patch("anymail_history.message.render_to_string", Mock(return_value=""))
class TestSendTemplatedMail(TestCase):
    def test_send_templated_email_anymail(self, mock_send):
        mock_send.return_value = 1

        email = send_templated_email(template_name="dummy_template_name")

        mock_send.assert_called_once()
        assert email is not None
        assert isinstance(email, HtmlAnymailMessage)

    def test_send_templated_email_anymail_api_error(self, mock_send):
        mock_send.side_effect = AnymailAPIError()

        assert send_templated_email(template_name="dummy_template_name") is None

        mock_send.assert_called_once()
