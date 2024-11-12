from rest_framework.serializers import ModelSerializer

from apps.shops.models import Product


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'