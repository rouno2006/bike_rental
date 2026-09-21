import os
import django
import random
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikerental.settings')
django.setup()

from rental.models import Brand, Bike

def populate():
    Bike.objects.all().delete()
    Brand.objects.all().delete()

    bikes_data = [
        # Existing Models
        {"brand": "Yamaha", "name": "R15 V4", "type": "gear", "cc": "155cc", "fuel": "Petrol", "price": 1200},
        {"brand": "Royal Enfield", "name": "Classic 350", "type": "gear", "cc": "350cc", "fuel": "Petrol", "price": 1500},
        {"brand": "Suzuki", "name": "Hayabusa", "type": "gear", "cc": "1340cc", "fuel": "Petrol", "price": 4500},
        {"brand": "Honda", "name": "Activa 6G", "type": "non_gear", "cc": "110cc", "fuel": "Petrol", "price": 500},
        {"brand": "Ola", "name": "S1 Pro", "type": "electric", "cc": "Motor", "fuel": "Electric", "price": 700},
        {"brand": "Kawasaki", "name": "Ninja ZX-10R", "type": "gear", "cc": "998cc", "fuel": "Petrol", "price": 4000},
        
        # New: Harley-Davidson Top Models
        {"brand": "Harley-Davidson", "name": "Fat Boy 114", "type": "gear", "cc": "1868cc", "fuel": "Petrol", "price": 5000},
        {"brand": "Harley-Davidson", "name": "Pan America 1250", "type": "gear", "cc": "1252cc", "fuel": "Petrol", "price": 4800},
        
        # New: Triumph Top Models
        {"brand": "Triumph", "name": "Rocket 3 R", "type": "gear", "cc": "2458cc", "fuel": "Petrol", "price": 6000},
        {"brand": "Triumph", "name": "Tiger 1200", "type": "gear", "cc": "1160cc", "fuel": "Petrol", "price": 4500},
        
        # New: Honda Gear Top Models
        {"brand": "Honda", "name": "CBR1000RR-R Fireblade", "type": "gear", "cc": "1000cc", "fuel": "Petrol", "price": 4200},
        {"brand": "Honda", "name": "Africa Twin Adventure", "type": "gear", "cc": "1084cc", "fuel": "Petrol", "price": 3800},
    ]

    colors = ["Midnight Black", "Racing Red", "Ocean Blue", "Matte Grey", "Pearl White"]

    for data in bikes_data:
        brand_obj, _ = Brand.objects.get_or_create(brand_name=data["brand"], about_brand="Premium Vehicles")
        
        for i in range(1, 4):
            # 100% Unique registration number logic
            unique_reg = f"WB-{random.randint(11, 99)}-{uuid.uuid4().hex[:4].upper()}"
            
            Bike.objects.create(
                bike_name=f"{data['name']} Edition {i}",
                bike_number=unique_reg,
                bike_type=data["type"],
                brand=brand_obj,
                model_year=2024,
                color=random.choice(colors),
                price_per_day=data["price"],
                cc=data["cc"],
                fuel=data["fuel"],
                seats='2',
                status='available',
                is_active=True
            )
            
    print("Premium Realistic Bikes Added Successfully!")

if __name__ == '__main__':
    populate()

    