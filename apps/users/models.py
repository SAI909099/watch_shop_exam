from django.contrib.auth.models import AbstractUser
from django.db.models import DateField, CharField, EmailField, BooleanField, ForeignKey, Model, CASCADE, \
    PositiveIntegerField, RESTRICT

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


