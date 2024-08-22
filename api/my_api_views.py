from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from . import models 
from . import serializers

@api_view(['GET'])
def check_username(request, username):
    try:
        User.objects.get(username=username)
        return Response({'exists': True})
    except User.DoesNotExist:
        return Response({'exists': False})


@api_view(['POST'])
def user_signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        models.CustomUser.objects.create(user=user)
        return Response({'success': True})
    except Exception as e:
        return Response({'success': False, 'error': str(e)})

@api_view(['GET'])
def show_requests(request):
    user = models.CustomUser.objects.get(user=request.user)
    requests = models.ShortRequest.objects.filter(user=user)
    data = serializers.ShortRequestSerializer(requests, many=True)
    
    return Response({'requests': data.data})

@api_view(['GET'])
def get_all_images_for_user(request, purpose):
    params = request.query_params 
        
    custom_user = models.CustomUser.objects.get(user=request.user)
    valid_values = [i[0] for i in models.image_purpose_choices]
    if purpose not in valid_values:
        print(purpose)
        return Response({'error': 'Invalid purpose'})
    if params.get('description'):
        description = params.get('description')
        images = models.ImageUpload.objects.filter(user=custom_user, purpose=purpose, description=description)
    else:
        images = models.ImageUpload.objects.filter(user=custom_user, purpose=purpose)
    data = serializers.ImageUploadSerializer(images, many=True)
    
    return Response({'images': data.data})

@api_view(['GET'])
def is_backer(request):
    if request.user.is_anonymous:
        return Response({'is_backer': False})
    user = models.CustomUser.objects.get(user=request.user)
    print(user)
    # check Backer model 
    user_is_backer = models.Backer.objects.filter(user=user).exists()
    print(models.Backer.objects.filter(user=user))
    print(user_is_backer)
    # input("Enter to coninue")
    if user_is_backer:
        return Response({'is_backer': True})
    return Response({'is_backer': False})

@api_view(['GET'])
def jobs_near_me(request):
    user = models.CustomUser.objects.get(user=request.user)

    # get preferred location from user
    backer = models.Backer.objects.get(user=user)

    # get details json
    details = backer.details
    """
    [{"topic": "About Me", "value": "Introduce yourself and why you enjoy being with pets"}, {"topic": "Pet Experience", "value": "Tell us about the type of pet you have and your experience with it"}, {"topic": "Your Skills and Qualifications", "value": ["Experience in training", "Behavioral modifications"]}, {"topic": "Other Skills", "value": "Other special skills with pet or qualifications"}, {"topic": "Service Name", "value": "Service Name"}, {"topic": "Listing Summary", "value": "Listing Summary"}, {"topic": "How many pets can you watch at your home at one time", "value": "3"}, {"topic": "Pets Accepted", "value": ["Dogs", "Cats", "Rabbits"]}, {"topic": "Size of Pets Accepted", "value": ["1-5 kg", "5-10 kg"]}, {"topic": "adult_supervision", "value": "Pets will never be left unattended"}, {"topic": "where pets left unsupervised", "value": "The garage area"}, {"topic": "where pets left at night", "value": "On my bed"}, {"topic": "Potty Breaks", "value": "3"}, {"topic": "Home you live in", "value": "Apartment/Condo"}, {"topic": "Size of outdoor area", "value": "Medium"}, {"topic": "Do you have transport emergencies", "value": "Yes"}, {"topic": "Do you allow last minute bookings", "value": "No"}, {"topic": "Preferred Search location", "value": "Preferred search location (Optional)"}, {"topic": "Service Type", "value": "Pet Boarding"}, {"topic": "price of service", "value": "3000"}, {"topic": "additional description of service", "value": "Pet owners will feel more comfortable knowing what is included in this quote"}, {"topic": "Apartment, house number", "value": "Apartment"}, {"topic": "Street Name", "value": "Sterret"}, {"topic": "City", "value": ",cmskjlbckaj"}, {"topic": "Zip Code", "value": "jdbvsjb"}, {"topic": "Country", "value": "jbdvjb"}, {"topic": "State", "value": "Odisha"}]
    """

    topic = "Search location for Service"
    # topic = "Preferred Search location"
    search_location = None
    for detail in details:
        if detail['topic'] == topic:
            search_location = detail['value']
            break
    if search_location is None:
        return Response({'error': 'Search location not found'})
    

    # get all the requests from the users in the same city
    question = "Where do you need the service?"
    # iterate thru request and get the location saved in data json field.
    # sample json file: [{"question": "service", "answer": "Pet Boarding"}, {"question": "How many pets do you need to board?", "answer": "2"}, {"question": "What type of pet it is?", "answer": ["dog", "cat"]}, {"question": "What breed is it?", "answer": "no"}, {"question": "What is the size of your pet?", "answer": ["1-5kg", "5-10kg"]}, {"question": "Anything else the sitter needs to know?", "answer": "no"}, {"question": "Please pick starting date of service?", "answer": "09:19, 2024-08-01"}, {"question": "Number of nights required?", "answer": "45"}, {"question": "Where do you need the service?", "answer": "hone"}, {"question": "Do you need pet pickup services?", "answer": "yes"}] 
    requests_near_user = []
    for request in models.Request.objects.all():
        data = request.data
        for d in data:
            if d['question'] == question:
                if d['answer'].lower() == search_location.lower():
                    requests_near_user.append(request)
                    break
    
    if not requests_near_user:
        return Response({'error': 'No requests found near you'})

    data = serializers.RequestSerializer(requests_near_user, many=True)
    return Response({'requests': data.data})

@api_view(['GET'])
def get_request_details_for_backer(request, request_id):
    user = models.CustomUser.objects.get(user=request.user)
    # if user is not backer, return error 
    if not models.Backer.objects.filter(user=user).exists():
        print("Not a backer")
        return Response({'error': 'User is not a backer'})
    try:
        request = models.Request.objects.get(id=request_id)
    except models.Request.DoesNotExist:
        return Response({'error': 'Request not found'})
    
    data = serializers.RequestSerializer(request)
    return Response({'request': data.data})