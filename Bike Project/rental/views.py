from django.contrib.auth.forms import AuthenticationForm
from .models import UserAddress
from .forms import AddressForm
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Bike, Brand, Booking
from .forms import BookingForm, CustomUserCreationForm

# 1. New Home Page
def home(request):
    return render(request, 'rental/home.html')

# 2. All Vehicles Page 
def vehicles(request):
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

# 3. Bikes Details and Booking 
def bike_detail(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Please login first to confirm your booking.")
            return redirect(f"/login/?next={request.path}")
            
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.bike = bike
            
            # Days and Fare Calculation
            days = (booking.to_date - booking.from_date).days
            if days <= 0: days = 1
            booking.total_amount = days * bike.price_per_day
            booking.booking_status = 'pending' 
            booking.save()
            
            # Before payment Add address 
            return redirect('address_selection', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'rental/bike_detail.html', {'bike': bike, 'form': form})


# New: Address Selection & Payment Processing
@login_required(login_url='login')
def address_selection(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    addresses = UserAddress.objects.filter(user=request.user) # User's Saved address
    
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        
        if selected_address_id:
            # If Old Address Select
            address = get_object_or_404(UserAddress, id=selected_address_id, user=request.user)
            booking.delivery_address = address
            booking.save()
        else:
            # If new Address type
            form = AddressForm(request.POST)
            if form.is_valid():
                new_address = form.save(commit=False)
                new_address.user = request.user
                new_address.save()
                booking.delivery_address = new_address
                booking.save()
            else:
                return render(request, 'rental/address_selection.html', {'booking': booking, 'addresses': addresses, 'form': form})
        
        # Address confirm and Open Razorpay Payment Page
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_amount = int(booking.total_amount * 100)
        
        payment_data = {
            "amount": razorpay_amount,
            "currency": "INR",
            "receipt": f"booking_{booking.id}",
        }
        razorpay_order = client.order.create(data=payment_data)
        
        context = {
            'booking': booking,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
            'razorpay_amount': razorpay_amount,
        }
        return render(request, 'rental/payment.html', context)
        
    else:
        form = AddressForm()
        
    context = {
        'booking': booking,
        'addresses': addresses,
        'form': form
    }
    return render(request, 'rental/address_selection.html', context)


# New: Payment Success Function
@csrf_exempt
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == "POST":
        booking.booking_status = 'booked' # After payment show status booked
        booking.save()
        messages.success(request, "Payment Successful! Your booking is confirmed.")
        return redirect('my_bookings')
    return redirect('home')

# 4. Booking HIstory
@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'rental/my_bookings.html', {'bookings': bookings})

# 5. Users Registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}! Your account has been created successfully.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'rental/register.html', {'form': form})

# 6. Custom Login Function
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            
            next_page = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_page)
    else:
        form = AuthenticationForm()
    return render(request, 'rental/login.html', {'form': form})

# 7. Booking Cancel
@login_required(login_url='login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST' and booking.booking_status == 'booked':
        booking.booking_status = 'cancelled'
        booking.save()
        messages.success(request, "Booking Cancelled!")
    return redirect('my_bookings')

def custom_logout(request):
    logout(request)
    messages.info(request, "You have been successfully logged out. See you soon!")
    return redirect('/')

def about_us(request):
    return render(request, 'rental/about.html')

def contact_us(request):
    if request.method == 'POST':
        messages.success(request, "Your message has been sent successfully! We will contact you soon.")
        return redirect('contact')
    return render(request, 'rental/contact.html')
