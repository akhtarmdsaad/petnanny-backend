from django.contrib import admin
from .models import *
from django.contrib.auth.models import User



# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Backer)
admin.site.register(Pet)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Availability)
admin.site.register(Payment)
admin.site.register(Message)
admin.site.register(MessageData)
# admin.site.register(ShortRequest)
admin.site.register(PetBoardingRequest)
admin.site.register(PetTrainingRequest)
admin.site.register(DogWalkingRequest)
admin.site.register(ImageUpload)
