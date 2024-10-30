from django import forms
from .models import User
from .models import Seller, Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'city_postal_code']


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['first_name', 'last_name', 'phone', 'email', 'comment']

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

        error_messages = {
            'username': {
                'required': 'This field is required',
                'max_length': 'The maximum number of characters is 150.',
            },
            'first_name': {
                'required': 'This field is required',
            },
            'last_name': {
                'required': 'This field is required',
            },
            'email': {
                'required': 'This field is required',
            },
            'password': {
                'required': 'This field is required',
            },
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
