# forms.py in voter app
from django import forms
from .models import Voter
from django import forms
from mongo_config import db


mohalla_name_collection = db['MohallaName']

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

    checked = forms.BooleanField(required=False, initial=False)

    # Mohalla name as a dropdown list
    mohalla_name = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Fetch mohalla names from the database
        mohalla_names = mohalla_name_collection.find({})
        print("Fetched Mohalla Names:", mohalla_names)
        # Populate choices with (id, name) for each entry
        self.fields['mohalla_name'].choices = [(mohalla['mohalla_name'], mohalla['mohalla_name']) for mohalla in mohalla_names]

class MohallaName(forms.Form):
    mohalla_name = forms.CharField(max_length=100, required=True)