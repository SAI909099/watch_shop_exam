from django.db import models
from django.db.models import CASCADE, CharField

from apps.users.models import User


class Categories(models.Model):
    name = CharField(max_length=50)

class Straps(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=CASCADE)

class Watches(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, CASCADE, related_name='products')
    about = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    case_color = models.CharField(max_length=50)
    dial_design = models.CharField(max_length=50)
    strap_design = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/%Y/%m/%d')


class CustomWatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    case_color = models.CharField(max_length=50)
    strap_color = models.CharField(max_length=50)
    dial_design = models.CharField(max_length=100)
    extra_strap = models.BooleanField(default=False)
    laser_engraving = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="custom_watches/", blank=True, null=True)

    def __str__(self):
        return f"Custom Watch by {self.user}"


