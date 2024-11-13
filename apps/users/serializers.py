from datetime import timedelta
from urllib.parse import urlparse

from allauth.account.utils import user_email
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField, HiddenField, CurrentUserDefault, IntegerField, BooleanField
from rest_framework.serializers import Serializer, ModelSerializer

from root import settings
from .models import User, Address, Country  # Import your custom User model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import redis

from ..shops.models import Product

redis_url = urlparse(settings.CELERY_BROKER_URL)


r = redis.StrictRedis(host=redis_url.hostname, port=redis_url.port, db=int(redis_url.path.lstrip('/')))

# --------------------Register---------------------------------------------------
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
        if data['email'] != data['confirm_email']:
            raise serializers.ValidationError("Email addresses do not match.")

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        # Remove fields that aren't part of the model
        validated_data.pop('confirm_email')
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data.get('date_of_birth'),
            phone_number=validated_data.get('phone_number'),
        )
        return user
# ------------------------------------Token----------------------------------

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

# -----------------------------------Login-------------------------------------

class LoginUserModelSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        redis_key = f'failed_attempts_{email}'
        attempts = r.get(redis_key)
        if attempts and int(attempts) >= 5:
            raise ValidationError("Too many failed login attempts. Try again after 5 minutes.")

        user = authenticate(email=email, password=password)

        if user is None:
            current_attempts = int(attempts) if attempts else 0
            r.setex(redis_key, timedelta(minutes=5), current_attempts + 1)
            raise ValidationError("Invalid email or password")

        r.delete(redis_key)
        attrs['user'] = user
        return attrs

# ---------------------------Address ------------------------------------------------


class CountryModelSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class AddressListModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    postal_code = IntegerField(default=123400, min_value=0)


    class Meta:
        model = Address
        exclude = ()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['country'] = CountryModelSerializer(instance.country).data
        return repr

