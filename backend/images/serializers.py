from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Image

class UploadImageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)   

    class Meta:
        model = Image        
        fields = [
            'image',
            'user',
        ]

class ListImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image        
        fields = [
            'id',
            'links',
            'date',            
        ]
