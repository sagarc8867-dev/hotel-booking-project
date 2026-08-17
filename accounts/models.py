from django.db import models

# This app intentionally has no models of its own.
# It uses Django's built-in User model for both guest and staff accounts,
# and links to guests.Guest for guest profile data.
