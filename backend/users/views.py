
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings


class LoginView(ObtainAuthToken):    
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})        
        serializer.is_valid(raise_exception=True)        
        user = serializer.validated_data['user']  
        login(request, user)       
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })
