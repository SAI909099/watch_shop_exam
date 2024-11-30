from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.shared.authenticated import CustomIsAuthenticated
from apps.shared.paginations import CustomPageNumberPagination
from apps.shops.models import Cart, CartItem, Order
from apps.shops.models import Watches, CustomWatch
from apps.shops.serializers import WatchListSerializer, CustomWatchSerializer, \
    AddCartItemSerializer, CartSerializer, OrderSerializer, OrderDetailSerializer
from apps.users.models import Card
import re

@extend_schema(tags=['watch_list'])
class WatchListApiView(ListAPIView):
    queryset = Watches.objects.all()
    serializer_class = WatchListSerializer
    permission_class = AllowAny,
    pagination_class = CustomPageNumberPagination


@extend_schema(tags=['custom_watch'])
class CustomWatchCreateApiView(CreateAPIView):
    queryset = CustomWatch.objects.all()
    serializer_class = CustomWatchSerializer
    authentication_classes = []
    permission_classes = [CustomIsAuthenticated, ]


# -------------------------------------

@extend_schema(tags=['Cart'])
class CartView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        total = cart.calculate_total()
        data = self.get_serializer(cart).data
        data['total'] = total
        return Response(data)

@extend_schema(tags=['Cart'])
class AddToCartView(CreateAPIView):
    serializer_class = AddCartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


@extend_schema(tags=['Cart'])
class UpdateCartItemView(UpdateAPIView):
    serializer_class = AddCartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)


@extend_schema(tags=['Cart'])
class RemoveCartItemView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

@extend_schema(tags=["Order"])
class OrderView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    # def post(self, request, *args, **kwargs):
    #     cart= Cart.objects.get_or_create(user=request.user)
    #
    #     card_number = request.data.get('card_number')
    #
    #     if not card_number:
    #         return Response({"error": "Card number is required."}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     # Prepare order data
    #     order_data = {
    #         'user': request.user,
    #         'cart': cart,
    #         'shipping_method': request.data.get('shipping_method'),
    #         'card_number': card_number,
    #     }
    #     order_serializer = OrderSerializer(data=order_data)
    #
    #     if order_serializer.is_valid():
    #         order_serializer.save()
    #         return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    #
    #     return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Order"])
class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)