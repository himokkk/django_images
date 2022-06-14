from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from images.serializers import ListImageSerializer, \
    UploadImageSerializer

from rest_framework import generics, status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication, TokenAuthentication

from rest_framework.settings import api_settings
from base64 import b64encode
import datetime
import pytz
from PIL import Image as Im
from io import BytesIO
import datetime
import os

from users.models import UserProfile
from images.models import Image, Link_Token
from .serializers import UserSerializer
from .permissions import IsImageOwner, ExpiringIsImageOwner
from .create_token import create_token


class TokenLinkView(APIView):
    def get(self, request, *args, **kwargs):
        string = kwargs['string']

        try:
            instance = Link_Token.objects.get(token=string)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        if instance is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
            
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
        id = int(string[0])
        requested_size = int(string[1])
        try:
            instance = Image.objects.get(id=id)
            profile = UserProfile.objects.get(user=request.user)
        except:
            HttpResponse(status=status.HTTP_204_NO_CONTENT) 

        if instance is None or profile is None: 
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
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
        id = int(string[0])
        delta_time = int(string[1])
        try:
            instance = Image.objects.get(id=id)
            profile = UserProfile.objects.get(user=request.user)
        except:
            HttpResponse(status=status.HTTP_204_NO_CONTENT)        

        if instance is None or profile is None:
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        tier = profile.tier
        min = int(tier.expiring.split("-")[0])
        max = int(tier.expiring.split("-")[1])
        if instance.user != request.user :
            return HttpResponse(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        if delta_time <= min and delta_time >= max:
                return HttpResponse(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        token = create_token(instance, int(string[1]), kwargs)                     
            
        return HttpResponseRedirect(redirect_to
        =f'http://localhost:8000/api/images/token/{token}')



class OriginalImageView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsImageOwner] 

    def get(self, request, *args, **kwargs): 
        id = int(kwargs["id"])

        instance = Image.objects.get(id=id)        
        profile = UserProfile.objects.get(user=request.user)

        if instance is None or profile is None:
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)        

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

    


    

    