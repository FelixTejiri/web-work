from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from dashboard.models import User

class RegisterForm(forms.ModelForm):

    error_messages={
        'password_mismatch':"The two password fields don't match.",
        'invalid_length':'Password length must be greater than 6 characters',
        'email_in_use':'An account is already registered with this email, please proceed to the <a href="/login"> login </a> area and login with account details.'
    }

    class Meta:
        model=User
        fields=['first_name','last_name','email']

    referrer=forms.IntegerField(
        label="Referrer ID",
        help_text="May leave empty if none",
        required=False
    )
        
    password=forms.CharField(
            label=('Password'),
            widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}),
            strip=False,
            help_text=password_validation.password_validators_help_text_html()
        )
        

    password2=forms.CharField(
        label=('Confirm Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}),
        help_text='Enter same password as before for verification'
    )

    def verify_passwords(self):
        password=self.cleaned_data.get('password')
        password2=self.cleaned_data.get('password2')

        if password != password2:
            confirm_pass=False
        else:
            confirm_pass=True 
        if len(password) < 6:
            pass_len=False
        else:
            pass_len=True
        return (confirm_pass,pass_len)

    def email_check(self):
        email=self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return True
        else:
            return False

    def save(self,commit=True):
        user=super().save(commit=False)
        password = self.cleaned_data.get('password2')
        user.set_password(password)
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):

    error_messages={
        'invalid_user':'Invalid Login Details. Please login with valid login details or register <a href="/register/"> here </a>',
        'unverified_user':'Your account is not yet verified, please check your mail for the verification link sent to you'
    } 

    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput, max_length=100)

    def verify_login(self):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return False
        else:
            if check_password(password,user.password):
                return user
            else:
                return False

class ContactForm(forms.Form):

    name=forms.CharField()
    email=forms.EmailField()
    subject=forms.CharField()
    message=forms.TextInput()
    
