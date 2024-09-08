from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: dict) -> AbstractUser:
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data: dict) -> None | dict:
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        raise serializers.ValidationError('Invalid credentials')