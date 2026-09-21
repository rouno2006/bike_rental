from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    drivelicense=models.CharField(max_length=50)
    mobile=models.CharField(max_length=12)

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    address_label = models.CharField(max_length=50, default="Home", help_text="e.g., Home, Office")
    full_address = models.TextField()
    
    def __str__(self):
        return f"{self.address_label} - {self.user.username}"
    
class Brand(models.Model):
    brand_name=models.CharField(max_length=255, verbose_name='Name of Brand')
    about_brand=models.CharField(max_length=255, verbose_name='Brand Description')
    def __str__(self):
        return self.brand_name
    
class Bike(models.Model):
    BIKE_TYPE_CHOICES = [
        ('gear', 'Gear'),
        ('non_gear', 'Non-Gear'),
        ('electric', 'Electric'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Maintenance'),
    ]

    bike_name = models.CharField(max_length=100)
    bike_number = models.CharField(max_length=20, unique=True)
    bike_type = models.CharField(
        max_length=20,
        choices=BIKE_TYPE_CHOICES
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model_year = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    cc=models.CharField(max_length=100)
    fuel=models.CharField(max_length=50)
    seats=models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='bikes/', blank=True, null=True)
    
    # NEW FIELDS ADDED HERE
    abs_function = models.BooleanField(default=False, help_text="True for Yes, False for No")
    mileage = models.CharField(max_length=50, help_text="e.g., 40 kmpl", blank=True, null=True)
    top_speed = models.CharField(max_length=50, help_text="e.g., 120 kmph", blank=True, null=True)

    def __str__(self):
        return f"{self.bike_name} ({self.bike_number})"

class Booking(models.Model):
    BOOKING_STATUS = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    bike = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE
    )

    from_date = models.DateField()
    to_date = models.DateField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    booking_status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default='booked'
    )
    delivery_address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True, blank=True)

    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bike.bike_name}"
    