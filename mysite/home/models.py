from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name= models.CharField(max_length=250)
    email= models.EmailField()
    subject= models.CharField(max_length=250)
    message= models.TextField()
    added_on= models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Contact Table"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profiles/%Y/%m/%d', null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural="Profile Table"