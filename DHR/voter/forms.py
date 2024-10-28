# forms.py in voter app
from django import forms
from .models import Voter

from django import forms

class VoterForm(forms.Form):
    government_number = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100)
    father_name = forms.CharField(max_length=100, required=True)
    
    # Gender as a dropdown list with choices
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    
    # CNIC with numeric validation
    cnic = forms.CharField(
        max_length=13,
        min_length=13,
        required=True,
        widget=forms.TextInput(attrs={'pattern': r'\d+', 'title': 'Numeric CNIC only'})
    )
    
    address = forms.CharField(max_length=250, required=True)
    
    # Mobile number with numeric validation
    mobile_number = forms.CharField(
        widget=forms.TextInput(attrs={'pattern': r'\d+', 'title': 'Numeric mobile number only'})
    )
    
    # Family code with numeric validation
    family_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'pattern': r'\d+', 'title': 'Numeric family code only'})
    )
    
    block_number = forms.CharField(max_length=10, required=False)