from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VoterForm
from django.views.decorators.csrf import csrf_exempt
from .models import Voter
import json
from mongo_config import db



# Create your views here.
voter_collection = db['voters']

@csrf_exempt
def add_voter(request):
    if request.method == 'GET':
        print("Getting Get Method")
        return render(request, 'voter/add_voter.html')

    if request.method == 'POST':
        print("Getting POST Method")
        form = VoterForm(request.POST)
        if form.is_valid():
            print("form is valid")
            # Auto-increment user_id
            max_user_id = voter_collection.find_one(sort=[("user_id", -1)])
            user_id = max_user_id['user_id'] + 1 if max_user_id else 1

            # Get form data
            voter_data = form.cleaned_data
            print("Form data:", voter_data)
            # Set family_code if not provided
            family_code = voter_data.get('family_code')
            if not family_code:
                family_code = user_id  # Set family_code to user_id if it’s empty
            
            # Prepare data for insertion
            new_voter = {
                "user_id": user_id,
                "government_number": voter_data['government_number'],
                "first_name": voter_data['first_name'],
                "last_name": voter_data['last_name'],
                "father_name": voter_data['father_name'],
                "gender": voter_data['gender'],
                "CNIC": voter_data['cnic'],
                "address": voter_data['address'],
                "mobile_number": voter_data['mobile_number'],
                "family_code": family_code,
                "block_number": voter_data['block_number']
            }

            # Insert the new voter into the database
            voter_collection.insert_one(new_voter)
            
            return JsonResponse({'message': 'Voter added successfully!'}, status=200)
        else:
            print("Form errors:", form.errors)  # This will show the specific field errors
            return JsonResponse({'message': 'Form is invalid', 'errors': form.errors}, status=400)
    else:
        form = VoterForm()
    return JsonResponse({'message': 'Error Occurred!'}, status=400)


def view_all_voter(request):
    # Fetch all voters from the MongoDB collection and sort them by name
    voters = list(voter_collection.find().sort('first_name', 1))  # Adjust field name if necessary

    # Optionally, you can convert MongoDB ObjectId to string for easier use in templates
    for voter in voters:
        voter['_id'] = str(voter['_id'])  # Convert ObjectId to string

    return render(request, 'voter/view_all_voter.html', {'voters': voters})


@csrf_exempt
def delete_voter(request, user_id):
    if request.method == "POST":
        try:
            # Attempt to delete the voter with the given user_id
            result = voter_collection.delete_one({'user_id': user_id})
            if result.deleted_count > 0:
                return JsonResponse({'success': True, 'message': 'Voter deleted successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Voter not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})    


@csrf_exempt
def update_voter(request, user_id):
    # Get the voter object using the user_id or return 404 if not found
    voter = voter_collection.find_one({'user_id': user_id})
    if not voter:
        return JsonResponse({'message': 'Voter not found'}, status=404)
    
    if request.method == 'POST':
        form = VoterForm(request.POST)
        if form.is_valid():
            # Prepare the updated voter data
            updated_data = {
                "government_number": form.cleaned_data['government_number'],
                "first_name": form.cleaned_data['first_name'],
                "last_name": form.cleaned_data['last_name'],
                "father_name": form.cleaned_data['father_name'],
                "gender": form.cleaned_data['gender'],
                "CNIC": form.cleaned_data['cnic'],  # Ensure this matches your form field name
                "address": form.cleaned_data['address'],
                "mobile_number": form.cleaned_data['mobile_number'],
                "family_code": form.cleaned_data.get('family_code') or user_id,  # Use user_id if family_code is empty
                "block_number": form.cleaned_data['block_number']
            }

            # Update the voter in the database
            voter_collection.update_one({'user_id': user_id}, {'$set': updated_data})
            return JsonResponse({'message': 'Voter updated successfully'}, status=200)

    else:
        # Prepopulate the form with voter's data
        initial_data = {
            "government_number": voter.get('government_number', ''),
            "first_name": voter.get('first_name', ''),
            "last_name": voter.get('last_name', ''),
            "father_name": voter.get('father_name', ''),
            "gender": voter.get('gender', ''),
            "cnic": voter.get('CNIC', ''),  # Make sure the key matches your form field name
            "address": voter.get('address', ''),
            "mobile_number": voter.get('mobile_number', ''),
            "family_code": voter.get('family_code', ''),
            "block_number": voter.get('block_number', '')
        }
        form = VoterForm(initial=initial_data)  # Use the initial_data to populate the form

    return render(request, 'voter/update_voter.html', {'form': form, 'voter': voter})