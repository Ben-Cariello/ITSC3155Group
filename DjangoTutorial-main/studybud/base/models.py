from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver



class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('employee', 'Employee'),
        ('business', 'Business'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='employee')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg', null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='employee')
    jobs_applied = models.CharField(max_length=100, null=True,blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Field(models.Model):
   name = models.CharField(max_length=200)

   def __str__(self):
      return self.name

class Job(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering = ['-updated', '-created']

    def __str__(self):
     return self.body[0:50]

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()