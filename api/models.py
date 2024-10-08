from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pics/')
    role = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Pet(models.Model):
    name = models.CharField(max_length=100,null=True)
    species = models.CharField(max_length=100)
    breed = models.CharField(max_length=100,null=True)
    age = models.IntegerField(null=True)
    size = models.CharField(max_length=100, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    diet = models.TextField(null=True)
    allergies = models.TextField(null=True)
    medical_conditions = models.TextField(null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    availability = models.BooleanField()

    def __str__(self):
        return self.name
    

class PetBoardingRequest(models.Model):
    service = models.CharField(max_length=50, default='Pet Boarding')
    num_pets = models.PositiveIntegerField()
    pet_type = models.TextField()
    pet_breed = models.CharField(max_length=50, blank=True, null=True)
    pet_size = models.TextField()
    additional_notes = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    num_nights = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    pickup_required = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.user.username + ' - ' + self.location


class DogWalkingRequest(models.Model):
    service = models.CharField(max_length=50, default='Dog Walking')
    num_dogs = models.PositiveIntegerField()
    dog_breed = models.CharField(max_length=50)
    dog_size = models.TextField()
    additional_notes = models.TextField(blank=True, null=True)
    walks_per_day = models.PositiveIntegerField()
    num_days = models.PositiveIntegerField()
    start_date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.user.username + ' - ' + self.location

class PetTrainingRequest(models.Model):
    service = models.CharField(max_length=50, default='Pet Training')
    num_pets = models.PositiveIntegerField()
    pet_type = models.TextField()
    pet_breed = models.CharField(max_length=50)
    pet_size = models.TextField()
    pet_age = models.TextField()
    course = models.TextField()
    training_type = models.CharField(max_length=50)
    additional_notes = models.TextField(blank=True, null=True)
    available_sessions = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.user.username + ' - ' + self.location

image_purpose_choices = (
    ('Profile', 'Profile'),
    ('Document', 'Document'),
    ('HomePics', 'HomePics'),
    ('PetPics', 'PetPics'),
    
)

class ImageUpload(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=100, choices= image_purpose_choices)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" {self.user.user.username} - {self.purpose} "

service_choices = (
    (1, 'Dog Trainer'),
    (2, 'Pet Boarding'),
    (3, 'Dog Walking'),
    
)

status_choices = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
)

# class ShortRequest(models.Model):
#     service = models.IntegerField(choices=service_choices)
#     start_date = models.DateField()
#     duration = models.IntegerField()        # in no of days 
#     location = models.CharField(max_length=100)
#     status = models.CharField(max_length=100, choices=status_choices, default='Pending')


#     def __str__(self):
#         return self.user.user.username + ' - ' + self.location


class Booking(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.pet.name + ' - ' + self.service.name
    
class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.booking.pet.name + ' - ' + self.booking.service.name

class BackerImages(models.Model):
    backer = models.ForeignKey('Backer', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='backer_images/')

    def __str__(self):
        return self.backer.user.user.username

class Backer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pics/')
    about_me = models.TextField(null=True)
    pet_experience = models.TextField(null=True)
    skills = models.CharField(max_length=255,null=True)  # Consider using a ListField if multiple skills are commo,null=Truen
    other_skills = models.TextField(null=True)
    service_name = models.CharField(max_length=100,null=True)
    listing_summary = models.TextField(null=True)
    max_pets = models.PositiveIntegerField(null=True)
    pets_accepted = models.CharField(max_length=255,null=True)  # Consider using a ListField
    pet_size = models.CharField(max_length=255,null=True)  # Consider using a ListField
    adult_supervision = models.CharField(max_length=100,null=True)
    unsupervised_location = models.CharField(max_length=100,null=True)
    nighttime_location = models.CharField(max_length=100,null=True)
    potty_breaks = models.PositiveIntegerField(null=True)
    home_type = models.CharField(max_length=100,null=True)
    outdoor_area_size = models.CharField(max_length=100,null=True)
    transport_emergencies = models.BooleanField(null=True)
    last_minute_bookings = models.BooleanField(null=True)
    preferred_location = models.CharField(max_length=100, default="Delhi")
    service_type = models.CharField(max_length=100,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    additional_description = models.TextField(null=True)
    apartment_house_number = models.CharField(max_length=50,null=True)
    street_name = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    zip_code = models.CharField(max_length=20,null=True)
    country = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.user.user.username 
  
class Availability(models.Model):
    backer = models.ForeignKey(Backer, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.backer.user.user.username

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.booking.pet.name + ' - ' + self.booking.service.name

# messages include text, photos, videos, etc.
class MessageData(models.Model):
    text = models.TextField()
    photo = models.ImageField(null=True, blank=True, upload_to='message_photos/')
    video = models.FileField(null=True, blank=True, upload_to='message_videos/')

    def __str__(self):
        return self.message.sender.user.username + ' to ' + self.message.recipient.user.username

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipient')
    message = models.ForeignKey(MessageData, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.user.username + ' to ' + self.recipient.user.username

# RIGHT NOW ITS OPTIONAL
# # Adding separate Role table to manage user roles
# class Role(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# # Adding separate Availability table to manage detailed availability
# class Availability(models.Model):
#     backer = models.ForeignKey(Backer, on_delete=models.CASCADE)
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     status = models.CharField(max_length=100)

#     def __str__(self):
#         return self.backer.user.user
    
# # Adding separate Payment table to manage payment details
# class Payment(models.Model):
#     booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=8, decimal_places=2)
#     payment_method = models.CharField(max_length=100)
#     status = models.CharField(max_length=100)

#     def __str__(self):
#         return self.booking.pet.name + ' - ' + self.booking.service.name

class Test(models.Model):
    name=models.CharField(max_length=100)