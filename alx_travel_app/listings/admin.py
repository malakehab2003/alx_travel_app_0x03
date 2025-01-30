from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Listing, Booking, Review

class CustomUserAdmin(UserAdmin):
    fieldsets = list(UserAdmin.fieldsets)
    
    if 'email' not in [field for fieldset in fieldsets for field in fieldset[1].get('fields', [])]:
        fieldsets.append(
            (None, {'fields': ('email',)})
        )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Listing)
admin.site.register(Booking)
admin.site.register(Review)
