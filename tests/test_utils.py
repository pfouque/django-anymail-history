from __future__ import annotations

from unittest.mock import Mock, patch

from django.template.exceptions import TemplateDoesNotExist
from django.test import TestCase

from anymail.exceptions import AnymailAPIError
from anymail.message import AnymailMessage

from anymail_history import send_templated_email


@patch("anymail.message.AnymailMessage.send")
class TestSendTemplatedMail(TestCase):
    @patch(
        "anymail_history.utils.render_to_string",
        Mock(side_effect=TemplateDoesNotExist("")),
    )
    def test_send_templated_email_template_not_found(self, mock_send):
        with self.assertRaises(TemplateDoesNotExist):
            send_templated_email(
                template_name="dummy_template_name",
            )

        mock_send.assert_not_called()

    @patch("anymail_history.utils.render_to_string")
    def test_send_templated_email_sent(self, mock_render_to_string, mock_send):
        mock_render_to_string.return_value = ""
        mock_send.return_value = 1

        email = send_templated_email(
            template_name="dummy_template_name",
        )

        mock_render_to_string.assert_called()
        mock_send.assert_called_once()
        assert isinstance(email, AnymailMessage)

    @patch("anymail_history.utils.render_to_string", Mock(return_value=""))
    def test_send_templated_email_anymail_api_error(self, mock_send):
        mock_send.side_effect = AnymailAPIError()

        email = send_templated_email(
            template_name="dummy_template_name",
        )

        mock_send.assert_called_once()
        assert email is None
