from django.db.models import CASCADE, CharField, Model, ForeignKey, TextField, DecimalField, ImageField,  \
    BooleanField
from django_jsonform.models.fields import JSONField

from apps.users.models import User


class Categories(Model):
    name = CharField(max_length=50)

    def __str__(self):
        return self.name


class Straps(Model):
    name = CharField(max_length=100)
    category = ForeignKey(Categories, on_delete=CASCADE)


class Watches(Model):
    SCHEMA = {
        'type': 'dict',
        'keys': {
            'keys': {
                'type': 'string',
                'title': 'Keys',
            },
            'coating': {
                'type': 'string',
                'title': 'Coating',
            },
            'glass':{
                'type': 'string',
                'title': 'Glass',
            },
            'straps':{
                'type': 'string',
                "title": "Straps",
            },
            'case_size':{
                'type': 'string',
                'title': 'Case size',
            },
            'case_color':{
                'type': 'string',
                'title': 'Case color',
            },
            'dial_color':{
                'type': 'string',
                'title': 'Dial color',
            },
            'water_resistance':{
                'type': 'string',
                'title': 'Water resistance',
            },
            'straps_type':{
                'type': 'string',
                "title": "Straps",
            },
            'movement':{
                'type':'string',
                'title':'Movement',
            },
            'instantaneous_rate':{
                'type': 'string',
                'title': 'Instantaneous rate',
            },
            'standard_battery_life':{
                'type': 'string',
                'title': 'Standard battery life',
            }

        }
    }
    name = CharField(max_length=100)
    category = ForeignKey(Categories, CASCADE, related_name='products')
    about = TextField()
    price = DecimalField(max_digits=5, decimal_places=2)
    case_color = CharField(max_length=50)
    dial_design = CharField(max_length=50)
    strap_design = CharField(max_length=50)
    image = ImageField(upload_to='products/%Y/%m/%d')
    specification = JSONField(schema=SCHEMA)

    def __str__(self):
        return self.name
from django.db import models
from django.db.models import Model, TextChoices, TextField, ManyToManyField, CharField
from rest_framework.fields import DecimalField


class CustomWatch(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    case_color = CharField(max_length=50)
    strap_color = CharField(max_length=50)
    dial_design = CharField(max_length=100)
    extra_strap = BooleanField(default=False)
    laser_engraving = BooleanField(default=False)
    price = DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Custom Watch by {self.user}"


class Product(Model):
    name = CharField(max_length=250)