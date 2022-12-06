from __future__ import annotations

from typing import Any

from django.template.loader import render_to_string

from anymail.exceptions import AnymailAPIError
from anymail.message import AnymailMessage
from anymail.utils import get_anymail_setting


def send_templated_email(
    template_name: str,
    context: dict[str, Any] | None = None,
    **kwargs: Any,
) -> AnymailMessage | None:
    # NOTE: https://anymail.dev/en/stable/tips/django_templates/#using-django-templates-for-email
    context = context or {}

    subject = kwargs.get("subject") or render_to_string(
        template_name=template_name.replace(".html", ".subject.txt"),
        context=context,
    ).replace("\n", "")

    email_message = AnymailMessage(
        subject=subject,
        **kwargs,
    )
    if get_anymail_setting("RENDER_HTML", default=True):
        email_message.attach_alternative(
            content=render_to_string(
                template_name=template_name,
                context=context,
            ),
            mimetype="text/html",
        )
    try:
        if email_message.send() != 0:
            return email_message
    except AnymailAPIError:
        pass
    return None
