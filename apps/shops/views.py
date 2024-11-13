from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from apps.shops.models import Product
from apps.shops.serializers import ProductModelSerializer


@extend_schema(tags=['product'])
class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer

