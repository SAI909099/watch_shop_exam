from datetime import timedelta
from urllib.parse import urlparse

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField
from rest_framework.serializers import Serializer

from root import settings
from .models import User  # Import your custom User model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import redis

redis_url = urlparse(settings.CELERY_BROKER_URL)


r = redis.StrictRedis(host=redis_url.hostname, port=redis_url.port, db=int(redis_url.path.lstrip('/')))


class RegisterUserModelSerializer(serializers.ModelSerializer):
    confirm_email = serializers.EmailField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'phone_number',
            'email', 'confirm_email', 'password', 'confirm_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        # Validate email and confirm_email match
        if data['email'] != data['confirm_email']:
            raise serializers.ValidationError("Email addresses do not match.")

        # Validate password and confirm_password match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        # Remove fields that aren't part of the model
        validated_data.pop('confirm_email')
        validated_data.pop('confirm_password')

        user = User.objects.create(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data.get('date_of_birth'),
            phone_number=validated_data.get('phone_number'),
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class LoginUserModelSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        redis_key = f'failed_attempts_{email}'
        attempts = r.get(redis_key)
        if attempts and int(attempts) >= 5:
            raise ValidationError("Too many failed login attempts. Try again after 5 minutes.")

        user = authenticate(username=email, password=password)

        if user is None:
            # If the users fails to authenticate, increase the count of failed attempts
            current_attempts = int(attempts) if attempts else 0
            r.setex(redis_key, timedelta(minutes=5), current_attempts + 1)  # Block for 5 minutes
            raise ValidationError("Invalid email or password")

            # If authentication is successful, reset the attempt counter
        r.delete(redis_key)
        attrs['users'] = user
        return attrs