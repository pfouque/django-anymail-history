from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import translation

from anymail.message import AnymailMessage

from anymail_history.utils import send_templated_email


class User(AbstractUser):
    language: str  # can be a CharField, a property or whatever valid LANGUAGE_CODE

    def send_templated_email(
        self,
        template_name: str,
        context: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> AnymailMessage:
        """
        Render and sends an email to this User.
        """
        context = context or {}
        context["recipient"] = self

        with translation.override(getattr(self, "language", settings.LANGUAGE_CODE)):
            return send_templated_email(
                template_name=template_name,
                context=context,
                to=[getattr(self, self.EMAIL_FIELD)],
                **kwargs,
            )
