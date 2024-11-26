from rest_framework.serializers import ModelSerializer

from apps.shops.models import Product


class ProductModelSerializer(ModelSerializer):
from rest_framework import serializers

from apps.shops.models import Watches, CustomWatch


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
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

