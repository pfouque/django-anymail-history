from __future__ import annotations

from typing import Any

from anymail.exceptions import AnymailAPIError

from .message import HtmlAnymailMessage


def send_templated_email(
    template_name: str,
    context: dict[str, Any] | None = None,
    *args: Any,
    **kwargs: Any,
) -> HtmlAnymailMessage | None:
    # NOTE: https://anymail.dev/en/stable/tips/django_templates/#using-django-templates-for-email

    email_message = HtmlAnymailMessage(template_name, context, *args, **kwargs)

    try:
        if email_message.send() != 0:
            return email_message
    except AnymailAPIError:
        pass
    return None
