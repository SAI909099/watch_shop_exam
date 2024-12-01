import random
import string
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from .models import Address, Country, ShippingMethod, Card, Contact
from .serializers import AddressListModelSerializer, \
    CountryModelSerializer, UserInfoSerializer, PasswordResetConfirmSerializer, \
    ForgotPasswordSerializer, ShippingMethodSerializer, CardSerializer, ContactSerializer, ForgetPasswordSerializer, \
    RegisterSerializer, LoginSerializer, LoginUserModelSerializer
from .tasks import send_verification_email


# ------------------------------------Register ------------------------------------------
@extend_schema(tags=['Login-Register'])
class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    # permission_classes = (AllowAny,)

    # Register a new user
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate a random 6-digit verification code
            verification_code = ''.join(random.choices(string.digits, k=6))
            user.reset_token = verification_code
            user.save()

            # Send the email asynchronously with Celery
            send_verification_email.delay(user.email, verification_code)

            return Response({"message": "User registered successfully. Check your email for the verification code."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.response import Response
@extend_schema(tags=['Login-Register'])
class VerifyEmailAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        # print("Request data:", request.data)  # Debugging the incoming data
        email = request.data.get('email')
        verification_code = request.data.get('verification_code') or request.data.get('password')  # Temporary fix

        # print("Request data:", request.data)  # This should now include 'verification_code'
        # print("Verification Code:", request.data.get('verification_code'))

        if not email or not verification_code:
            return Response({"error": "Email and verification code are required."}, status=400)

        try:
            user = User.objects.get(email=email, reset_token=verification_code)
            user.is_active = True
            user.reset_token = ''
            user.save()
            return Response({"message": "Email verified successfully."}, status=200)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or verification code."}, status=400)

@extend_schema(tags=['Login-Register'])
class LoginAPIView(GenericAPIView):
    serializer_class = LoginUserModelSerializer
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

@extend_schema(tags=['Access-Token'])
class ActivateUserView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            uid, is_active = uid.split('/')
            user = User.objects.get(pk=uid, is_active=is_active)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "User successfully verified!"})
        raise AuthenticationFailed('The link is invalid or expired.')

#-------------------------------Forgot password---------------------------------
class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)
# --------------------
# views.py
class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
# ----------------------------------User info -------------------------------


@extend_schema(tags=['user'])
class UserInfoListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

# ----------------------------------Address----------------------------------------

@extend_schema(tags=['address'])
class AddressListCreateAPIView(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressListModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@extend_schema(tags=['address'])
class AddressDestroyUpdateAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressListModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        self._can_delete = qs.count() > 1
        return qs

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)



@extend_schema(tags=['address'])
class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
    authentication_classes = ()
# -------------------------------------- shipping   ---------------------------------------

@extend_schema(tags=['shipping-methods'])
class ShippingMethodListView(ListAPIView):
    queryset = ShippingMethod.objects.all()
    serializer_class = ShippingMethodSerializer

# ---------------------------------------payment ----------------------------
@extend_schema(tags=['card'])
class ValidateCardAPIView(APIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = IsAuthenticated,

    def post(self, request):
        data = request.data
        serializer = CardSerializer(data=data)
        if serializer.is_valid():
            valid_thru = serializer.validated_data['valid_thru']
            if valid_thru < datetime.now().date():
                return Response({"error": "Card has expired."}, status=status.HTTP_400_BAD_REQUEST)

            # Validation successful
            return Response({"message": "Card is valid!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------------contact us ----------------------------

@extend_schema(tags=['Contact us'])
class ContactAPIView(APIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Contact saved successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# --------------------------forgot password -------------------------

@extend_schema(tags=['forget password'])
class ForgetPasswordAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = ForgetPasswordSerializer

    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response({"error": "This email is not active."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)


User = get_user_model()


class ResetPasswordAPIView(APIView):
    def post(self, request, uid, token):
        new_password = request.data.get('password')
        if not new_password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"error": "Invalid user ID"}, status=status.HTTP_404_NOT_FOUND)

        # Verify the token
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)

