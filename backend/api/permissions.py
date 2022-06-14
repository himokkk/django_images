from rest_framework import permissions
from images.models import Image


class IsImageOwner(permissions.BasePermission):
    message = 'Not your Image.'

    def has_permission(self, request, view):
        image_id = view.kwargs["id"]
        instance = Image.objects.get(id=image_id) 
        if instance is None:
           return False
        if instance.user != request.user:
            return False
        return True

class ExpiringIsImageOwner(permissions.BasePermission):
    message = 'Not your Image.'

    def has_permission(self, request, view):
        image_id = int(view.kwargs["string"].split("-")[0])
        instance = Image.objects.get(id=image_id) 
        if instance is None:
           return False
        if instance.user != request.user:
            return False
        return True