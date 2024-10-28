from django import forms

class SuperuserForm(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())