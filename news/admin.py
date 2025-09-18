from django.contrib import admin
from .models import Source, Article
from unfold.admin import ModelAdmin


@admin.register(Source)
class SourceAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "rss_feed_url",
        "country",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "id", "rss_feed_url", "country")
    ordering = ("-created_at",)


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ("id", "title", "source", "published_at", "created_at", "updated_at")
    list_display_links = ("id", "title")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "id", "source")
    ordering = ("-published_at",)
