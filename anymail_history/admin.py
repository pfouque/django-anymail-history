from __future__ import annotations

from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from .models import MessageEvent, SentMessage


class ReadonlyInline(admin.TabularInline):
    can_delete = False
    show_change_link = False
    extra = 0

    def has_add_permission(
        self, request: HttpRequest, obj: SentMessage | None = None
    ) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: SentMessage | None = None
    ) -> bool:
        return False


class MessageEventInline(ReadonlyInline):
    model = MessageEvent
    readonly_fields = fields = ("event_name", "created_on")
    ordering = ["-created_on"]


@admin.register(SentMessage)
class SentMessageAdmin(admin.ModelAdmin):
    ordering = ["-created_on"]
    inlines = [
        MessageEventInline,
    ]

    def has_add_permission(
        self, request: HttpRequest, obj: SentMessage | None = None
    ) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: SentMessage | None = None
    ) -> bool:
        return False

    def get_actions(self, request: HttpRequest) -> dict[str, Any]:
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


class SentMessageInline(ReadonlyInline):
    model = SentMessage
    readonly_fields = fields = ("message_id", "subject", "status")
    ordering = ["-created_on"]
