from django.contrib import admin
from .models import CustomUser, Brand, Bike, Booking

admin.site.register(CustomUser)
admin.site.register(Brand)
admin.site.register(Bike)
admin.site.register(Booking)