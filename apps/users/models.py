from datetime import timedelta
import random

from django.contrib.auth.models import AbstractUser
from django.db.models import DateField, CharField, EmailField, BooleanField, ForeignKey, Model, CASCADE, \
    PositiveIntegerField, RESTRICT, DecimalField, TextChoices, DateTimeField
from django.utils.timezone import now

from .manager import CustomUserManager
from ..shared.models import TimeBasedModel


class User(AbstractUser):
    username = None
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    date_of_birth = DateField(null=True, blank=True)
    phone_number = CharField(max_length=15, null=True, blank=True)
    email = EmailField(unique=True)
    is_active = BooleanField(default=False)
    reset_token = CharField(max_length=64, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

class Country(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Address(TimeBasedModel):
    user = ForeignKey('User', RESTRICT)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    phone_number = CharField(max_length=15)
    address_line_1 = CharField(max_length=255)
    address_line_2 = CharField(max_length=255, null=True, blank=True)
    city = CharField(max_length=255)
    postal_code = PositiveIntegerField(default=0)
    country = ForeignKey(Country, CASCADE)




class ShippingMethod(Model):
    class ShippingType(TextChoices):
        STANDARD = 'standard', 'Standard'
        EXPRESS = 'express', 'Express'

    name = CharField(
        max_length=20,
        choices=ShippingType.choices,
        default=ShippingType.STANDARD
    )
    price = DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} - ${self.price}"
# ------------------------------Card------------------------------------------------



class Card(Model):
    card_number = CharField(max_length=16, unique=True)
    valid_thru = DateField()
    card_name = CharField(max_length=100)
    user = ForeignKey('User',CASCADE)

    def __str__(self):
        return self.card_name

# ------------------contact us ------------------------

class Contact(Model):
    firs_name = CharField(max_length=250)
    email = EmailField()
    maessage = CharField()

#===============login register ============

class VerificationCode(Model):
    email = EmailField(unique=True)
    code = CharField(max_length=6)
    created_at = DateTimeField(auto_now_add=True)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=10)

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))
