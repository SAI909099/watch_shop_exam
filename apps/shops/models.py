from django.db.models import CASCADE, Model, ForeignKey, ImageField, \
    BooleanField, DateTimeField, PositiveIntegerField,TextField, CharField,DecimalField
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
            'glass': {
                'type': 'string',
                'title': 'Glass',
            },
            'straps': {
                'type': 'string',
                "title": "Straps",
            },
            'case_size': {
                'type': 'string',
                'title': 'Case size',
            },
            'case_color': {
                'type': 'string',
                'title': 'Case color',
            },
            'dial_color': {
                'type': 'string',
                'title': 'Dial color',
            },
            'water_resistance': {
                'type': 'string',
                'title': 'Water resistance',
            },
            'straps_type': {
                'type': 'string',
                "title": "Straps",
            },
            'movement': {
                'type': 'string',
                'title': 'Movement',
            },
            'instantaneous_rate': {
                'type': 'string',
                'title': 'Instantaneous rate',
            },
            'standard_battery_life': {
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
    specification = JSONField(schema=SCHEMA)

    def __str__(self):
        return self.name

class ImagesModel(Model):
    watches = ForeignKey(Watches, on_delete=CASCADE, related_name='images')
    image = ImageField(upload_to='products/%Y/%m/%d')

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


#
# class Product(Model):
#     name = CharField(max_length=250)

# --------------------------bilol ----------------------------------

class Cart(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name="cart")
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user}"


class CartItem(Model):
    cart = ForeignKey(Cart, on_delete=CASCADE, related_name="items")
    watch = ForeignKey(Watches, on_delete=CASCADE)
    quantity = PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.watch.name} in {self.cart}"
