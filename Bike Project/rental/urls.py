from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bike/<int:bike_id>/', views.bike_detail, name='bike_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),    
    path('logout/', views.custom_logout, name='logout'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('payment-success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('address-selection/<int:booking_id>/', views.address_selection, name='address_selection'),
]
