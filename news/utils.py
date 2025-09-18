import feedparser
from .models import Source, Article
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime


def fetch_and_store_articles():
    """Fetch articles from all sources and store them in the database."""

    sources = Source.objects.all()

    for source in sources:
        print(f"Fetching articles from {source.name}...")

        feed = feedparser.parse(source.rss_feed_url)

        print(f"Found {len(feed.entries)} entries.")

        print(f"First entry: {feed.entries[0]}")

        new_articles = []

        for entry in feed.entries:

            # Ensure published date is timezone-aware
            published_at = None
            if hasattr(entry, "published"):
                published_at = parse_datetime(entry.published)
                if published_at and not published_at.tzinfo:
                    published_at = make_aware(published_at)

            # skip if article with same original_url already exists
            if Article.objects.filter(original_url=entry.link).exists():
                continue

            article = Article.objects.create(
                source=source,
                title=entry.title,
                original_url=entry.link,
                published_at=published_at or make_aware(parse_datetime(entry.updated)),
                description=getattr(entry, "summary", ""),
                content=getattr(entry, "content", [{"value": ""}])[0]["value"],
                image=getattr(entry, "media_content", [{"url": ""}])[0]["url"],
            )

            new_articles.append(article)

        print(f"Stored {len(new_articles)} new articles from {source.name}.")
