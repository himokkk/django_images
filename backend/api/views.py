from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from django.shortcuts import get_object_or_404

import pytz
from PIL import Image as Im
from io import BytesIO
import datetime

from users.models import UserProfile
from images.models import Image, Link_Token

from images.serializers import ListImageSerializer, \
    UploadImageSerializer
from .serializers import UserSerializer

from .permissions import IsImageOwner, ExpiringIsImageOwner
from .create_token import create_token


class TokenLinkView(APIView):
    def get(self, request, *args, **kwargs):
        string = kwargs['string']

        instance = get_object_or_404(Link_Token, token=string)        

        utc = pytz.UTC
        now = utc.localize(datetime.datetime.now())
        date = instance.expiration_time
        if date < now:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        image = instance.image.image
        return HttpResponse(image, content_type="image/jpeg")
        
    

class ThumbnailView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsImageOwner] 

    def get(self, request, *args, **kwargs):
        string = kwargs['string'].split("-")
        image_id = int(string[0])
        requested_size = int(string[1])
        instance = get_object_or_404(Image, id=image_id) 
        profile = get_object_or_404(UserProfile, user=request.user)
    
        sizes = profile.tier.thumbnail_sizes.split(' ') 
        for size in sizes:
            if int(size) == requested_size:                 
                image = Im.open(instance.image)        
                resize = (requested_size, requested_size)
                membuf = BytesIO()
                image.thumbnail(resize)
                image.save(membuf, format="jpeg")
                return HttpResponse(membuf.getvalue(),
                content_type="image/jpeg") 
        return HttpResponse() 



class ExpireView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ExpiringIsImageOwner] 

    def get(self, request, *args, **kwargs):        
        string = kwargs['string'].split("-")
        image_id = int(string[0])
        delta_time = int(string[1])
        image = get_object_or_404(Image, id=image_id)
        profile = get_object_or_404(UserProfile, user=request.user)     

        tier = profile.tier
        min = int(tier.expiring.split("-")[0])
        max = int(tier.expiring.split("-")[1])
        if image.user != request.user :
            return HttpResponse(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        if delta_time <= min and delta_time >= max:
                return HttpResponse(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        token = create_token(image, int(string[1]), kwargs)                     
            
        return HttpResponseRedirect(redirect_to
        =f'http://localhost:8000/api/images/token/{token}')



class OriginalImageView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsImageOwner] 

    def get(self, request, *args, **kwargs): 
        image_id = int(kwargs["id"])

        instance = get_object_or_404(Image, id=image_id)        
        profile = get_object_or_404(UserProfile, user=request.user) 

        if profile.tier.link_to_original == 1:
            return HttpResponse(instance.image, content_type="image/jpeg") 

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



class List_Images(generics.ListAPIView): 
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]   

    serializer_class = ListImageSerializer

    def get_queryset(self):
        queryset = Image.objects.all().filter(user=self.request.user)
        return queryset

    
    
class Upload_Image(generics.ListCreateAPIView): 
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Image.objects.all()   
    serializer_class = UploadImageSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    


    

    