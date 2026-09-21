from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, CustomUser
from .models import UserAddress

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'username' , 'mobile' , 'email']

class BookingForm(forms.ModelForm):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label="Pickup Date")
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label="Drop Date")

    class Meta:
        model = Booking
        fields = ['from_date', 'to_date']


class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['address_label', 'full_address']
        widgets = {
            'address_label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Home, Office, Hostel'}),
            'full_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your full delivery address...'}),
        }
        
        