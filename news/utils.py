import feedparser
from .models import Source, Article
from django.utils.timezone import make_aware, now
from django.utils.dateparse import parse_datetime
from django.utils.text import slugify
import time

rss_sources = [
    # Nigerian Tech Feeds
    {"name": "Technext", "url": "https://technext.ng/feed", "country": "Nigeria"},
    {"name": "TechCabal", "url": "https://techcabal.com/feed", "country": "Nigeria"},
    {"name": "Techpoint Africa", "url": "https://techpoint.africa/feed", "country": "Nigeria"},
    {"name": "TechCity", "url": "https://techcityng.com/feed", "country": "Nigeria"},
    {"name": "Tech Build Africa", "url": "https://techbuild.africa/feed", "country": "Nigeria"},
    {"name": "Tech Digest News", "url": "https://techdigest.ng/feed", "country": "Nigeria"},
    {"name": "Nairametrics", "url": "https://nairametrics.com/feed/", "country": "Nigeria"},
    {"name": "Ventureburn", "url": "https://ventureburn.com/feed/", "country": "Nigeria"},
    {
        "name": "Nigerian Tribune Tech",
        "url": "https://tribuneonlineng.com/category/technology/feed/",
        "country": "Nigeria",
    },
    {"name": "Business Day Tech", "url": "https://businessday.ng/technology/feed/", "country": "Nigeria"},
    {"name": "Tech Next", "url": "https://technext.ng/feed/", "country": "Nigeria"},
    {"name": "IT News Africa", "url": "https://www.itnewsafrica.com/feed/", "country": "Nigeria"},
    {
        "name": "Nigerian Communications Week",
        "url": "https://www.nigeriacommunicationsweek.com.ng/feed/",
        "country": "Nigeria",
    },
    {"name": "Condia", "url": "https://thecondia.com/feed/", "country": "Nigeria"},
    {"name": "Innovation Village", "url": "https://innovation-village.com/feed/", "country": "Nigeria"},
    # International Tech Feeds
    {"name": "Wired", "url": "https://www.wired.com/feed/category/science/latest/rss", "country": "USA"},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed", "country": "USA"},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "country": "USA"},
    {"name": "CNET", "url": "https://www.cnet.com/rss/how-to", "country": "USA"},
    {"name": "Ars Technica", "url": "https://arstechnica.com/feed/", "country": "USA"},
]


def create_sources_from_rss():
    """
    Create Source objects from a list of predefined RSS feed sources.
    """

    sources_list = []

    for src in rss_sources:
        d = feedparser.parse(src["url"])

        if not d.entries:
            print(f"No entries found for {src['name']}, skipping...")
            continue  # skip if no entries found
        # if d.bozo:  # feed is broken
        #     print(f"❌ Invalid RSS feed: {src['url']}")
        #     continue  # skip this one

        # Create Source instance (but don't save yet)
        slug = slugify(src["name"])[:100]
        source = Source(
            name=src["name"] or d.feed.title,
            slug=slug,
            rss_feed_url=src["url"],
            logo=d.feed.image.href if hasattr(d.feed, "image") else None,
            country=src["country"],
        )
        print(f"Parsed RSS feed: {src['name']}")
        sources_list.append(source)

    # Bulk create sources, ignoring conflicts
    saved_sources = Source.objects.bulk_create(sources_list, ignore_conflicts=True)
    print(f"Created {len(saved_sources)} new sources.")

    return saved_sources


def fetch_and_store_articles():
    """Fetch articles from all sources and store them in the database."""

    # Start timer
    start_time = time.time()

    sources = Source.objects.all()

    print("===" * 20)
    for source in sources:
        print(f"Fetching articles from {source.name}...")

        feed = feedparser.parse(source.rss_feed_url)
        print(f"Found {len(feed.entries)} entries.")

        # get all existing article URLs for this source to avoid duplicates
        existing_urls = set(Article.objects.filter(source=source).values_list("original_url", flat=True))

        new_articles = []

        for entry in feed.entries:

            # skip if article already exists
            if entry.link in existing_urls:
                continue

            # Ensure published date is timezone-aware
            published_at = None
            if hasattr(entry, "published"):
                published_at = parse_datetime(entry.published)
            elif hasattr(entry, "updated"):
                published_at = parse_datetime(entry.updated)
            # Fallback: set to now if nothing worked
            if published_at:
                if not published_at.tzinfo:
                    published_at = make_aware(published_at)
            else:
                published_at = now()

            # Create the Article instance (but don't save yet)
            slug = slugify(entry.title)[:100]

            article = Article(
                source=source,
                title=entry.title,
                slug=slug,
                original_url=entry.link,
                published_at=published_at or make_aware(parse_datetime(entry.updated)),
                description=getattr(entry, "summary", ""),
                content=getattr(entry, "content", [{"value": ""}])[0]["value"],
                image=getattr(entry, "media_thumbnail", [{"url": ""}])[0].get("url", ""),
            )

            new_articles.append(article)

        # Bulk create new articles if any
        print(f"Storing {len(new_articles)} new articles...")
        if new_articles:
            saved_articles = Article.objects.bulk_create(new_articles, ignore_conflicts=True)
            print(f"Stored {len(saved_articles)} new articles from {source.name}.")
        print("===" * 20)

    # End timer
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Total time taken to fetch and store articles: {elapsed_time:.2f} seconds")
