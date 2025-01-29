from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = "Seeds the database with sample listings data."

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database with sample data...")

        host, created = User.objects.get_or_create(username="sample_host", email="host@example.com")
        if created:
            self.stdout.write("Created sample host.")

        sample_listings = [
            {
                "title": "Cozy Apartment",
                "description": "A small but comfortable apartment in the city center.",
                "price_per_night": 100.00,
                "location": "New York"
            },
            {
                "title": "Beach House",
                "description": "A beautiful house overlooking the ocean.",
                "price_per_night": 300.00,
                "location": "Malibu"
            },
        ]

        Listing.objects.all().delete()
        self.stdout.write("Deleted existing listings.")

        for listing_data in sample_listings:
            listing = Listing.objects.create(**listing_data, host=host)
            self.stdout.write(f"Created listing: {listing.title}")

        self.stdout.write("Database seeding complete!")
