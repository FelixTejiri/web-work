from django import forms

from .models import User,ProofOfPayment
from mainsite.models import  InvestmentPlan

class UserInformationChangeForm(forms.ModelForm):

    error_messages={
        'invalid_input':'Please fill out the change form with valid input.',
    } 

    class Meta:
        model=User
        fields=['first_name','last_name','email','phone_number']

    def save(self,commit=False):
        user=super().save(commit=False)
        if commit:
            user.save()
        return user

class BankForm(forms.ModelForm):

    class Meta:
        model=User
        fields=['bank_name','bank_account_number','bank_account_name']

class UploadForm(forms.ModelForm):

    class Meta:
        model=ProofOfPayment
        fields=['amount','investment_plan','file','extra']

class PasswordChangeForm(forms.Form):

    error_messages={
        'password_mismatch':"The two password fields don't match.",
        'invalid_length':'Password length must be greater than 6 characters',
        'invalid_input':'Please fill out the change form with valid input.',
        'wrong_password':'The old password field does not correspond with the current user password'
    }

    old_password=forms.CharField(
        widget=forms.PasswordInput(),
        label='Old Password')
    new_password=forms.CharField(
        widget=forms.PasswordInput(),
        label="New Password")
    confirm_password=forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password")

    def verify_passwords(self):
        password=self.cleaned_data.get('new_password')
        password2=self.cleaned_data.get('confirm_password')

        if password != password2:
            confirm_pass=False
        else:
            confirm_pass=True
        if len(password) < 6:
            pass_len=False
        else:
            pass_len=True
        return confirm_pass,pass_len