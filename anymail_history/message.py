from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from anymail.message import AnymailMessage
from anymail.utils import get_anymail_setting
from django.core.mail import EmailMultiAlternatives
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from html2text import html2text

if TYPE_CHECKING:

    class MultiAlternativesMixin(EmailMultiAlternatives):
        ...

else:

    class MultiAlternativesMixin:
        ...


class HtmlMessageMixin(MultiAlternativesMixin):
    def __init__(
        self,
        template_name: str,
        context: dict[str, Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        context = context or {}

        html_body = render_to_string(
            template_name=template_name,
            context=context,
        )

        if not kwargs.get("subject"):
            kwargs["subject"] = render_to_string(
                template_name=template_name.replace(".html", ".subject.txt"),
                context=context,
            ).replace("\n", "")

        if not kwargs.get("body"):
            try:
                kwargs["body"] = render_to_string(
                    template_name=template_name.replace(".html", ".txt"),
                    context=context,
                )
            except TemplateDoesNotExist:
                print("EXCEPT")
                if get_anymail_setting("HTML2TEXT", default=False):
                    kwargs["body"] = html2text(html_body)

        super().__init__(*args, **kwargs)

        self.attach_alternative(content=html_body, mimetype="text/html")


class HtmlEmailMessage(HtmlMessageMixin, EmailMultiAlternatives):
    pass


class HtmlAnymailMessage(HtmlMessageMixin, AnymailMessage):
    pass
