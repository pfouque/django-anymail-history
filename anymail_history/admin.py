from __future__ import annotations

from django.contrib import admin
from django.http import HttpRequest

from .models import MessageEvent
from .models import SentMessage


class ReadonlyInline(admin.TabularInline):
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
    fields = ("event_name", "created_on")
    readonly_fields = fields
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


class SentMessageInline(ReadonlyInline):
    model = SentMessage
    fields = ("message_id", "subject", "status")
    readonly_fields = fields
    ordering = ["-created_on"]
