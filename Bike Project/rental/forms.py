from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, CustomUser

# Customers Registrasiton Form
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('mobile', 'drivelicense')

# Booking Form
class BookingForm(forms.ModelForm):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label="Pickup Date")
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label="Drop Date")

    class Meta:
        model = Booking
        fields = ['from_date', 'to_date']