from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ("id", "is_superuser", "email", "first_name", "last_name", "username", "is_verified", "created_at", "updated_at")
    list_display_links = ("id", "email", "first_name", "last_name", "username")
    search_fields = ("email", "first_name", "last_name", "username", "id")
    ordering = ("is_superuser",)