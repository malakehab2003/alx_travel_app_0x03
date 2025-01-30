from django.shortcuts import render
from rest_framework import viewsets
from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .tasks import send_booking_email
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
    
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request):
        property_id = request.data.get('property_id')
        user_id = request.data.get('user_id')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        total_price = request.data.get('total_price')

        property = get_object_or_404(Listing, listing_id=property_id)
        user = get_object_or_404(User, id=user_id)

        booking = Booking.objects.create(
            property_id=property,
            user_id=user,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price
        )

        booking.save()

        send_booking_email.delay(booking.id)

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

