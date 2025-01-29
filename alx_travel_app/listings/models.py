from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Listing(models.Model):
    """Model for a property listing."""
    title = models.CharField(max_length=255, help_text="Title of the listing")
    description = models.TextField(help_text="Detailed description of the listing")
    price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Price per night for the listing"
    )
    location = models.CharField(max_length=255, help_text="Location of the property")
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    """Model for a booking associated with a listing."""
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name="bookings", 
        help_text="Listing being booked"
    )
    guest = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="bookings", 
        help_text="Guest making the booking"
    )
    check_in_date = models.DateField(help_text="Check-in date")
    check_out_date = models.DateField(help_text="Check-out date")
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Total price for the booking"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(check_out_date__gt=models.F('check_in_date')),
                name="check_out_after_check_in"
            )
        ]

    def __str__(self):
        return f"Booking by {self.guest.username} for {self.listing.title}"


class Review(models.Model):
    """Model for a review for a listing."""
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name="reviews", 
        help_text="Listing being reviewed"
    )
    reviewer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="reviews", 
        help_text="User writing the review"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    comment = models.TextField(blank=True, help_text="Review comment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.listing.title}"
