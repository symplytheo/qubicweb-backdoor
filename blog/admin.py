from django.contrib import admin
from .models import Category, Post
from unfold.admin import ModelAdmin
from django import forms
from tinymce.widgets import TinyMCE


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("id", "name", "slug", "created_at", "updated_at")
    list_display_links = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "id")
    ordering = ("-created_at",)


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))

    class Meta:
        model = Post
        fields = "__all__"


@admin.register(Post)
class PostAdmin(ModelAdmin):
    form = PostForm
    list_display = ("id", "title", "category", "created_at", "updated_at")
    list_display_links = ("id", "title")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "id", "category")
    ordering = ("-created_at",)
