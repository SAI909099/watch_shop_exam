from datetime import timedelta
from urllib.parse import urlparse

import redis
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import HiddenField, CurrentUserDefault, IntegerField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from root import settings
from .models import User, Address, Country, ShippingMethod, Card, Contact

redis_url = urlparse(settings.CELERY_BROKER_URL)


r = redis.StrictRedis(host=redis_url.hostname, port=redis_url.port, db=int(redis_url.path.lstrip('/')))

# --------------------Register---------------------------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(write_only=True)

# -----------------------------Forgot password -----------------------

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                raise ValidationError("This email is not active.")
        except User.DoesNotExist:
            raise ValidationError("This email does not exist.")
        return email

from django.contrib.auth.password_validation import validate_password

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data


#---------------------------------User info -------------------------------

class UserInfoSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            "first_name" , "last_name" , "email"
        ]

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

# ---------------------------password reset -----------------------

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return email

    def save(self):
        request = self.context.get('request')
        user = User.objects.get(email=self.validated_data['email'])
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Generate reset link
        reset_link = f"{request._current_scheme_host}/reset-password/{uid}/{token}/"

        # Send reset email (you can adjust email settings in your project)
        user.email_user(
            subject="Password Reset Request",
            message=f"Click the link below to reset your password:\n{reset_link}",
            from_email=None  # Use default from_email from settings
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = urlsafe_base64_decode(data['uid']).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError("Invalid UID or user does not exist.")

        if not PasswordResetTokenGenerator().check_token(user, data['token']):
            raise ValidationError("Invalid or expired token.")

        self.user = user
        return data

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()

# -----------------------------------shipping-------------------

class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'price']

# -----------------------------------payment ----------------------


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_number', 'valid_thru', 'card_name']


# ----------------------------Contact---------------------------------

class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        exclude = ()

