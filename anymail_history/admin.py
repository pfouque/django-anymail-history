from __future__ import annotations

from collections.abc import Sequence

from django.contrib import admin
from django.http import HttpRequest

from .models import SentMessage, SentMessageEvent


class SentMessageEventInline(admin.TabularInline):
    model = SentMessageEvent
    readonly_fields = fields = ("event_name", "created_on")
    ordering = ["-created_on"]

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

    def get_readonly_fields(
        self, request: HttpRequest, obj: SentMessage | None = None
    ) -> Sequence[str]:
        return self.fields


@admin.register(SentMessage)
class SentMessageAdmin(admin.ModelAdmin):
    ordering = ["-created_on"]
    inlines = [SentMessageEventInline]

    def has_add_permission(
        self, request: HttpRequest, obj: SentMessage | None = None
    ) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: SentMessage | None = None
    ) -> bool:
        return False

    def get_readonly_fields(
        self, request: HttpRequest, obj: SentMessage | None = None
    ) -> Sequence[str]:
        return self.fields
