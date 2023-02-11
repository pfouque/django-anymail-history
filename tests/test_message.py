from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from django.core.mail import EmailMultiAlternatives
from django.template.exceptions import TemplateDoesNotExist
from django.test import TestCase
from django.test import override_settings

from anymail_history.message import HtmlEmailMessage


def html_does_not_exist(template_name: str, context: dict[str, Any]):
    if template_name.endswith(".html"):
        raise TemplateDoesNotExist("")
    return "html_version"


def subject_does_not_exist(template_name: str, context: dict[str, Any]):
    if template_name.endswith(".subject.txt"):
        raise TemplateDoesNotExist("")
    return "subject"


def text_does_not_exist(template_name: str, context: dict[str, Any]):
    if template_name.endswith(".txt") and not template_name.endswith(".subject.txt"):
        raise TemplateDoesNotExist("")
    return "text_version"


class TestHtmlEmailMessage(TestCase):
    @patch(
        "anymail_history.message.render_to_string",
        MagicMock(side_effect=html_does_not_exist),
    )
    def test_template_not_found__html(self):
        with self.assertRaises(TemplateDoesNotExist):
            HtmlEmailMessage(
                template_name="dummy_template_name.html",
            )

    @patch(
        "anymail_history.message.render_to_string",
        MagicMock(side_effect=subject_does_not_exist),
    )
    def test_template_not_found__subject(self):
        with self.assertRaises(TemplateDoesNotExist):
            HtmlEmailMessage(
                template_name="dummy_template_name.html",
            )

    @patch(
        "anymail_history.message.render_to_string",
        MagicMock(side_effect=text_does_not_exist),
    )
    def test_template_not_found__txt(self):
        email = HtmlEmailMessage(
            template_name="dummy_template_name.html",
        )
        assert email.body == ""

    @override_settings(ANYMAIL_HTML2TEXT=True)
    @patch("anymail_history.message.html2text", Mock(return_value="txt_from_html"))
    @patch(
        "anymail_history.message.render_to_string",
        MagicMock(side_effect=text_does_not_exist),
    )
    def test_template_not_found__txt_from_html(self):
        email = HtmlEmailMessage(
            template_name="dummy_template_name.html",
        )
        assert email.body == "txt_from_html"

    @patch("anymail_history.message.render_to_string")
    def test_send_templated_email_context(self, mock_render_to_string):
        mock_render_to_string.return_value = "{{ my_variable }} is Awesome"

        email = HtmlEmailMessage(
            template_name="dummy_template_name", context={"my_variable": "interpolated"}
        )

        mock_render_to_string.assert_called_with(
            template_name="dummy_template_name", context={"my_variable": "interpolated"}
        )
        assert isinstance(email, EmailMultiAlternatives)
        assert len(email.alternatives) == 1
        # FIXME: test template rendering
        # html_alternative = email.alternatives[0]
        # assert html_alternative[0] == "interpolated is Awesome"
