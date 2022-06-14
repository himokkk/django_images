from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def upload_to(instance, file_name):
    return 'media/{filename}'.format(filename=file_name)

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="image_owner")
    links = models.CharField(max_length=1000, default="{}", blank = True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default = 'media/1.jpeg')

    def __str__(self):
        return f"Image of id {self.id}"

class Link_Token(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, default=1, related_name="image_token")
    token = models.CharField(max_length=100, default="", null=True)
    expiration_time = models.DateTimeField(null=True, blank=True)