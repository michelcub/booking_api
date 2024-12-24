from rest_framework.serializers import ModelSerializer
from .models import User, Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ["full_name", "avatar", "address"]


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]
