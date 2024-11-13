from rest_framework import serializers

from apps.shops.models import Watches, CustomWatch


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watches
        fields = '__all__'

class CustomWatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomWatch
        fields = '__all__'