from django.db import models
from django.db.models import Model, TextChoices, TextField, ManyToManyField, CharField
from rest_framework.fields import DecimalField



class Product(Model):
    name = CharField(max_length=250)