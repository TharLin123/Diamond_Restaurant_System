from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from .models import Profile,Staff,OrderFood,CustomerPayment,FoodCart,Customer

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,label='Email')

    class Meta:
        model = Customer    
        fields = (
            'username',
            'gender',
            'dob',
            'address',
            'phone_number',
            'email',
            'password1',
            'password2'
        )
        widgets = {
            'username': forms.TextInput()
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Customer
        fields = ['username','gender','dob','address','phone_number','email']
    
    def save(self):
        super().save()



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
    
    def save(self):
        super().save()


class FoodCartForm(forms.ModelForm):
    customer = forms.CharField(disabled=True)

    class Meta:
        model = FoodCart
        fields = ['customer','food_to_order']
    
    def save(self):
        super().save()


class FoodOrderForm(forms.ModelForm):   
    class Meta:
        model = OrderFood
        fields = ['quantity']


class PaymentForm(forms.ModelForm):
    total_price = forms.IntegerField(widget=forms.HiddenInput(), initial="value")


    class Meta:
        model = CustomerPayment
        fields = ['payment_method','name_on_card','card_number','customer','total_price','food_cart']

    def save(self):
        super().save()