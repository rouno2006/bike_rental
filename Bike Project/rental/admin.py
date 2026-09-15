from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Bike, Booking

admin.site.register(Brand)
admin.site.register(Booking)

# Custom Admin
class BikeAdmin(admin.ModelAdmin):
    list_display = ('bike_name', 'bike_number', 'image_tag', 'price_per_day') 

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="50" style="border-radius:5px;" />', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Bike Image'

admin.site.register(Bike, BikeAdmin)
