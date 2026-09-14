from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bike, Brand, Booking
from .forms import BookingForm, CustomUserCreationForm

# 3. Home Page
def home(request):
    type_filter = request.GET.get('type')
    bike_types = Bike.BIKE_TYPE_CHOICES
    
    if type_filter:
        bikes = Bike.objects.filter(bike_type=type_filter, is_active=True, status='available')
    else:
        bikes = Bike.objects.filter(is_active=True, status='available')
        
    return render(request, 'rental/index.html', {
        'bikes': bikes, 
        'bike_types': bike_types, 
        'selected_type': type_filter
    })

# 2. Bikes Details and Booking
@login_required(login_url='login')
def bike_detail(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.bike = bike
            
            # Days and Fare Calculetion
            days = (booking.to_date - booking.from_date).days
            if days <= 0: days = 1
            booking.total_amount = days * bike.price_per_day
            booking.booking_status = 'booked'
            booking.save()
            
            messages.success(request, "Booking Successful!")
            return redirect('my_bookings')
    else:
        form = BookingForm()
    
    return render(request, 'rental/bike_detail.html', {'bike': bike, 'form': form})

# 3. Booking HIstory
@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'rental/my_bookings.html', {'bookings': bookings})

# 4. Booking Cancel
@login_required(login_url='login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST' and booking.booking_status == 'booked':
        booking.booking_status = 'cancelled'
        booking.save()
        messages.success(request, "Booking Cancelled!")
    return redirect('my_bookings')

# 5. Users Registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'rental/register.html', {'form': form})