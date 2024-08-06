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
    
class Request(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # status = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user.username

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

class ShortRequest(Request):
    service = models.IntegerField(choices=service_choices)
    start_date = models.DateField()
    duration = models.IntegerField()        # in no of days 
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=status_choices, default='Pending')


    def __str__(self):
        return self.user.user.username + ' - ' + self.location

class PetSitterRequest(Request):
    no_of_pets = models.IntegerField()
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    visit_times_per_day = models.IntegerField() 
    start_date = models.DateField()     
    duration = models.IntegerField()        # in no of days
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.pet.name + ' - ' + self.location

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pics/')
    bio = models.TextField()
    experience = models.TextField()
    skills = models.TextField()


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
    


    