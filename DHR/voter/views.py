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
    # return JsonResponse({'message': 'Error Occured!!'})
    # try:
    #     # Parse the JSON data from the request body
    #     voter_data = json.loads(request.body)
        
    #     # Create a new Voter object
    #     voter = Voter(
    #         government_number=voter_data.get('government_number'),
    #         name=voter_data.get('name'),
    #         father_name=voter_data.get('father_name'),
    #         gender=voter_data.get('gender'),
    #         CNIC=voter_data.get('CNIC'),
    #         address=voter_data.get('address'),
    #         mobile_number=voter_data.get('mobile_number'),
    #         family_code=voter_data.get('family_code') or None  # Set to None if empty
    #     )
        
    #     # Save the voter to the database
    #     voter.save()
        
    #     return JsonResponse({"message": "Voter added successfully!"}, status=201)
    # except json.JSONDecodeError:
    #     return JsonResponse({"error": "Invalid JSON"}, status=400)
    # except Exception as e:
    #     return JsonResponse({"error": str(e)}, status=400)

def view_all_voter(request):
    voters = Voter.objects.all().order_by('name')  # Fetch all voters, ordered alphabetically by name
    return render(request, 'voter/view_all_voter.html', {'voters': voters})
@csrf_exempt
def delete_voter(request, VoterID):
    if request.method == "POST":
        try:
            voter = Voter.objects.get(VoterID=VoterID)
            voter.delete()
            return JsonResponse({'success': True, 'message': 'Voter deleted successfully'})
        except Voter.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Voter not found'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def update_voter(request, VoterID):
    # Get the voter object using the VoterID or return 404 if not found
    voter = get_object_or_404(Voter, VoterID=VoterID)
    
    if request.method == 'POST':
        form = VoterForm(request.POST, instance=voter)
        if form.is_valid():
            form.save()  # Save the updated voter details
            return JsonResponse({'message': 'Voter updated successfully'}, status=200)
    else:
        form = VoterForm(instance=voter)  # Prepopulate the form with voter's data
    
    return render(request, 'voter/update_voter.html', {'form': form, 'voter': voter})



