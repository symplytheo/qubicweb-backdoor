from django.core.management.base import BaseCommand
from news.utils import fetch_and_store_articles, create_sources_from_rss


class Command(BaseCommand):
    help = "Populate the database with RSS feed sources and articles."

    def handle(self, *args, **options):

        self.stdout.write("Starting to populate RSS feeds...")

        # First, create sources from predefined RSS links
        self.stdout.write("Creating sources from RSS feeds...")
        sources = create_sources_from_rss()
        self.stdout.write(f"Finished creating {len(sources)} sources successfully.")

        print("===" * 20)

        # Then, fetch and store articles from these sources
        self.stdout.write("Fetching and storing articles from sources...")
        fetch_and_store_articles()
        self.stdout.write(self.style.SUCCESS("Successfully populated RSS feeds and articles."))
