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
    custom_user = models.CustomUser.objects.get(user=request.user)
    valid_values = [i[0] for i in models.image_purpose_choices]
    if purpose not in valid_values:
        print(purpose)
        return Response({'error': 'Invalid purpose'})
    images = models.ImageUpload.objects.filter(user=custom_user, purpose=purpose)
    data = serializers.ImageUploadSerializer(images, many=True)
    
    return Response({'images': data.data})