from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class RegistroForm(UserCreationForm):
    first_name= forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=30, required=True )


    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8 or not any(c.isdigit() for c in password1) or not any(c.isupper() for c in password1) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError("¡La contraseña debe cumplir con los requerimientos!")
        return password1
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("¡El nombre de usuario ya existe, preuba con otro!")
        return username
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
