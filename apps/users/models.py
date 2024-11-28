from django.contrib.auth.models import AbstractUser
from django.db.models import DateField, CharField, EmailField, BooleanField, ForeignKey, Model, CASCADE, \
    PositiveIntegerField, RESTRICT, DecimalField

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
    STANDARD = 'Standard'
    EXPRESS = 'Express'

    SHIPPING_METHOD_CHOICES = [
        (STANDARD, 'Standard'),
        (EXPRESS, 'Express'),
    ]

    name = CharField(
        max_length=20,
        choices=SHIPPING_METHOD_CHOICES,
        default=STANDARD,
    )
    price = DecimalField(max_digits=6, decimal_places=2, default=0.00)  # Price for express, 0 for standard

    def __str__(self):
        return f"{self.name} - ${self.price}"

# ------------------------------Card------------------------------------------------



class Card(Model):
    card_number = CharField(max_length=16, unique=True)
    valid_thru = DateField()
    card_name = CharField(max_length=100)

    def __str__(self):
        return self.card_name
# ------------------contact us ------------------------

class Contact(Model):
    firs_name = CharField(max_length=250)
    email = EmailField()
    maessage = CharField()

