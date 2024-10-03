import datetime
from django.shortcuts import render
from django.db.models import Q
from .models import *
from rest_framework import viewsets 
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import os
import shutil

def save_image(image):
    # Get the file name
    file_name = image.name

    # create model instance of ImageUpload
    image_instance = ImageUpload(image=image)
    image_instance.save()

  


# Create your views here.
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class BackerViewSet(viewsets.ModelViewSet):
    queryset = Backer.objects.all()
    serializer_class = BackerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        custom_user = CustomUser.objects.get(user=user)
        return Backer.objects.filter(user=custom_user)
    

    def perform_create(self, serializer):
        user = CustomUser.objects.get(user=self.request.user)
        serializer.save(user=user)

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDataViewSet(viewsets.ModelViewSet):
    queryset = MessageData.objects.all()
    serializer_class = MessageDataSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class ShortRequestViewSet(viewsets.ModelViewSet):
#     queryset = ShortRequest.objects.all()
#     serializer_class = ShortRequestSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         user = CustomUser.objects.get(user=self.request.user)
#         serializer.save(user=user)

class PetBoardingRequestViewSet(viewsets.ModelViewSet):
    queryset = PetBoardingRequest.objects.all()
    serializer_class = PetBoardingRequestSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.id:
            return PetBoardingRequest.objects.all()
        custom_user = CustomUser.objects.get(user=user)
        is_backer = Backer.objects.filter(user=custom_user).exists()
        if is_backer:
            pref_location = Backer.objects.get(user=custom_user).preferred_location
            return PetBoardingRequest.objects.filter(location=pref_location)
        elif custom_user:
            return PetBoardingRequest.objects.filter(user=custom_user.id)
        else:
            return PetBoardingRequest.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = PetBoardingRequest.objects.get(pk=kwargs['pk'])
            user = request.user
            if not user.id:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            custom_user = CustomUser.objects.get(user=user)
            is_backer = Backer.objects.filter(user=custom_user).exists()
            
            if instance.user == custom_user or is_backer:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except PetBoardingRequest.DoesNotExist:
            return Response({'error': 'PetBoardingRequest not found'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        user = CustomUser.objects.get(user=self.request.user)
        serializer.save(user=user)

class PetTrainingRequestViewSet(viewsets.ModelViewSet):
    queryset = PetTrainingRequest.objects.all()
    serializer_class = PetTrainingRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        custom_user = CustomUser.objects.get(user=user)
        is_backer = Backer.objects.filter(user=custom_user).exists()
        if is_backer:
            return PetTrainingRequest.objects.all()
        else:
            return PetTrainingRequest.objects.filter(user=custom_user)

    def perform_create(self, serializer):
        user = CustomUser.objects.get(user=self.request.user)
        serializer.save(user=user)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = PetTrainingRequest.objects.get(pk=kwargs['pk'])
            user = request.user
            custom_user = CustomUser.objects.get(user=user)
            is_backer = Backer.objects.filter(user=custom_user).exists()
            
            if instance.user == custom_user or is_backer:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except PetTrainingRequest.DoesNotExist:
            return Response({'error': 'PetTrainingRequest not found'}, status=status.HTTP_404_NOT_FOUND)

class DogWalkingRequestViewSet(viewsets.ModelViewSet):
    queryset = DogWalkingRequest.objects.all()
    serializer_class = DogWalkingRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        custom_user = CustomUser.objects.get(user=user)
        is_backer = Backer.objects.filter(user=custom_user).exists()
        
        if is_backer:
            return DogWalkingRequest.objects.all()
        else:
            return DogWalkingRequest.objects.filter(user=custom_user)


    def perform_create(self, serializer):
        user = CustomUser.objects.get(user=self.request.user)
        serializer.save(user=user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        custom_user = CustomUser.objects.get(user=user)
        is_backer = Backer.objects.filter(user=custom_user).exists()

        if instance.user == custom_user or is_backer:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'error': 'Unauthorized'}, status=401)


class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=CustomUser.objects.get(user=request.user))

        return Response(serializer.data)
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = CustomUser.objects.get(user=self.request.user)
        serializer.save(user=user)
        
        
        
    
