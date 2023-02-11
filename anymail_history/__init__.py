from __future__ import annotations

from .message import HtmlAnymailMessage
from .message import HtmlEmailMessage
from .utils import send_templated_email

__all__ = [
    "HtmlEmailMessage",
    "HtmlAnymailMessage",
    "send_templated_email",
]
