from __future__ import annotations

from django.apps import AppConfig


class AnymailHistoryConfig(AppConfig):
    name = "anymail_history"
    verbose_name = "Anymail History"

    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        from . import receivers  # noqa: F401
