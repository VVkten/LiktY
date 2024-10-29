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
                'required': 'Це поле обов\'язкове.',
                'max_length': 'Максимальна кількість символів — 150.',
            },
            'first_name': {
                'required': 'Це поле обов\'язкове.',
            },
            'last_name': {
                'required': 'Це поле обов\'язкове.',
            },
            'email': {
                'required': 'Це поле обов\'язкове.',
            },
            'password': {
                'required': 'Це поле обов\'язкове.',
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
