from .models import User,Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)