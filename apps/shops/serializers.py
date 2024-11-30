from decimal import Decimal

from rest_framework import serializers
from rest_framework.fields import IntegerField, CurrentUserDefault, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer

from apps.shops.models import Cart, CartItem, Order
from apps.shops.models import Watches, CustomWatch
from apps.users.models import ShippingMethod


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watches
        fields = '__all__'

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

        cart = validated_data.pop('cart')
        watch = validated_data.pop('watch')
        quantity = validated_data.pop('quantity')
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, watch=watch, defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item

    def update(self, instance, validated_data):
        # Handle updating the CartItem quantity
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance



class CartItemSerializer(ModelSerializer):
    watch = StringRelatedField()

    class Meta:
        model = CartItem
        fields = ['id', 'watch', 'quantity']


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items']


class OrderSerializer(serializers.ModelSerializer):
    user = CurrentUserDefault()
    class Meta:
        model = Order
        fields = ['shipping_method', 'card', 'cart', 'user']

    def create(self, validated_data):
        shipping_method = validated_data.get('shipping_method')
        cart = validated_data['cart']

        item_total = sum(item.watch.price * item.quantity for item in cart.items.all())
        shipping_cost = Decimal('0.00')
        if shipping_method.name == ShippingMethod.ShippingType.EXPRESS:
            shipping_cost = shipping_method.price

        total_amount = item_total + shipping_cost

        order = Order.objects.create(total_amount=total_amount, **validated_data)
        return order


class OrderDetailSerializer(ModelSerializer):
    shipping_method = StringRelatedField()
    user = StringRelatedField()
    cart_items = SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart_items', 'shipping_method', 'total_amount', 'created_at']

    def get_cart_items(self, obj):
        return [
            {
                'watch': item.watch.name,
                'quantity': item.quantity,
                'price': item.watch.price,
            }
            for item in obj.cart.items.all()
        ]