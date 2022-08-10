from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer
from django.contrib.auth.models import User

class CustomTokenObtainSerializer(TokenObtainPairSerializer):    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['user'] = UserSerializer(self.user,many=False).data
        return data
