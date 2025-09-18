from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        "id",
        "is_staff",
        "email",
        "first_name",
        "last_name",
        "username",
        "is_verified",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "email", "first_name", "last_name", "username")
    search_fields = ("email", "first_name", "last_name", "username", "id")
    ordering = ("-is_staff",)


# remove Group model from admin as we are not using it
admin.site.unregister(Group)
