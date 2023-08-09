from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "phone_number",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    ]
    list_filter = ["is_staff", "is_superuser", "groups"]
    search_fields = ["email"]
    search_help_text = "Email"

    fieldsets = (
        (None, {"fields": ("password", "last_login")}),
        (
            "Personal Info",
            {
                "fields": (
                    "email",
                    "phone_number",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")},
        ),
    )
