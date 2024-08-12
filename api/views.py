import datetime
from django.shortcuts import render
from .models import *
from rest_framework import viewsets 
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        # check if user parameter is given in the request

        user = CustomUser.objects.get(user=self.request.user)
        print(user)
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

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    # allow for filtering based on user
    # def get_queryset(self):
    #     user = self.request.user
    #     return Request.objects.filter(user=user)

    def perform_create(self, serializer):
        # check if user parameter is given in the request

        user = CustomUser.objects.get(user=self.request.user)
        print(user)
        serializer.save(user=user)

class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=CustomUser.objects.get(user=request.user))

        return Response(serializer.data)