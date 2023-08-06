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
    list_filter = ["is_staff", "is_superuser"]
    search_fields = ["email"]
    search_help_text = "Email"
