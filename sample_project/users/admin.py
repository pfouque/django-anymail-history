from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from anymail_history.admin import SentMessageInline


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [
        SentMessageInline,
    ]
