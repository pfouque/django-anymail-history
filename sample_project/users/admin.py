from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from anymail_history.admin import SentMessageInline

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [
        SentMessageInline,
    ]
