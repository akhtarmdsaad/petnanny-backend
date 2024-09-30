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
    # check Backer model 
    user_is_backer = models.Backer.objects.filter(user=user).exists()
    if user_is_backer:
        return Response({'is_backer': True})
    return Response({'is_backer': False})

@api_view(['GET'])
def show_requests_to_user(request):
    user = models.CustomUser.objects.get(user=request.user)
    petboarding_requests = models.PetBoardingRequest.objects.filter(user=user).order_by('-created_at')
    pettraining_requests = models.PetTrainingRequest.objects.filter(user=user).order_by('-created_at')
    dogwalking_requests = models.DogWalkingRequest.objects.filter(user=user).order_by('-created_at')
    

    data = {
        'petboarding_requests': serializers.PetBoardingRequestSerializer(petboarding_requests, many=True).data,
        'pettraining_requests': serializers.PetTrainingRequestSerializer(pettraining_requests, many=True).data,
        'dogwalking_requests': serializers.DogWalkingRequestSerializer(dogwalking_requests, many=True).data,
    }

    return Response(data)

@api_view(['GET'])
def jobs_near_me(request):
    user = models.CustomUser.objects.get(user=request.user)
    try:
        backer = models.Backer.objects.get(user=user)
    except models.Backer.DoesNotExist:
        return Response({'error': 'User is not a backer'})
    location = backer.preferred_location
    petboarding_requests = models.PetBoardingRequest.objects.filter(location=location)
    pettraining_requests = models.PetTrainingRequest.objects.filter(location=location)
    dogwalking_requests = models.DogWalkingRequest.objects.filter(location=location)

    data = {
        'petboarding_requests': serializers.PetBoardingRequestSerializer(petboarding_requests, many=True).data,
        'pettraining_requests': serializers.PetTrainingRequestSerializer(pettraining_requests, many=True).data,
        'dogwalking_requests': serializers.DogWalkingRequestSerializer(dogwalking_requests, many=True).data,
    }  

    return Response(data)
