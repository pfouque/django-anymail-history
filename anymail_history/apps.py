from __future__ import annotations

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = "anymail_history"
    verbose_name = "Anymail History"

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    def ready(self) -> None:
        from . import receivers  # noqa
