from django import forms
from .models import Order, Customer
from django.contrib.auth.models import  User
from django.views.generic import FormView


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_by', 'shipping_address', 'mobile', 'email']


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'first_name', 'middle_name', 'last_name', 'address']

    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("Username already exist")
        return uname

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())



