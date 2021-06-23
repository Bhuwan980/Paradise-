from django import forms
from .models import Order, Customer, Product, ProudctImage
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

class ProductCreateForm(forms.ModelForm):
    more_image = forms.FileField(required=False, widget = forms.FileInput(attrs={
        'class': 'form-control',
        'multiple': True
    }))
    class Meta:
        model = Product
        fields = ['name','desc', 'price', 'slug', 'category',
                  'warranty', 'return_policy', 'image']
        widgets = {
            'name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Product Name'
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder':'Description of Proudct',
                'rows':4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder':'Enter the pirce of the proudct'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the unique title '
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'warranty': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Enter the warrenty of the Product'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'return_policy': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Return Policy'
            }),
        }





