from unicodedata import category

from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField, SlugRelatedField
from rest_framework.serializers import ModelSerializer

from apps.shops.models import Cart, CartItem, Categories
from apps.shops.models import Watches, CustomWatch

class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = 'name',

class WatchListSerializer(serializers.ModelSerializer):
    category_name = SlugRelatedField(source='category',slug_field='name', read_only=True)

    class Meta:
        model = Watches
        fields = ['price', 'name', 'category_name']


class CustomWatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomWatch
        exclude = 'user',

    def save(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


# ------------------------------------------------
class AddCartItemSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(
        queryset=Watches.objects.all(), source="watch"
    )
    quantity = IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'quantity']

    def create(self, validated_data):
        # Handle the creation of the CartItem
        cart = validated_data.pop('cart')
        watch = validated_data.pop('watch')
        quantity = validated_data.pop('quantity')
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, watch=watch, defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity  # Update the quantity if the item exists
            cart_item.save()
        return cart_item

    def update(self, instance, validated_data):
        # Handle updating the CartItem quantity
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


class CartItemSerializer(ModelSerializer):
    watch = StringRelatedField()  # You can replace this with `WatchesSerializer` if needed.

    class Meta:
        model = CartItem
        fields = ('id', 'watch', 'quantity',)


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Include related cart items

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items']  # List cart fields and nested items


class WatchDetailSerializer(ModelSerializer):
    category_name = CategoryModelSerializer(read_only=True)\

    class Meta:
        model = Watches
        fields = ('name', 'category_name','price','about','case_color','dial_design',
                  'strap_design','specification',
                  )