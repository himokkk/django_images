from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

from .models import UserProfile
from images.models import Image


@receiver(post_save, sender = User)
def update_profile(sender, instance,**kwargs):
   user = UserProfile.objects.get_or_create(user=instance)
      

@receiver(post_save, sender = UserProfile)
def update_profile(sender, instance, **kwargs):   
   tier = instance.tier
   sizes = instance.tier.thumbnail_sizes.split(' ')
   base_url = settings.BASE_URL + 'api/images/'

   for image in Image.objects.filter(user=instance.user):      
      id = str(image.id)
      string = ""
      if tier.link_to_original == 1:         
         string += f'original size image: {base_url}media/{id} '

      for size in sizes:
         string+= f'{size}px thumbnail: {base_url}thumbnail/{id}-{size} '         

      if len(tier.expiring) > 2:
            sizes = tier.expiring.split('-')

      if len(sizes) >= 2:
         min, max = sizes
         string += f'expiring link: {base_url}create-expiring/{id}-(int)  + choose time from {min} to {max} seconds. '
            
      image.links = string
      image.save()
   