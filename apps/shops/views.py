from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.shared.authenticated import CustomIsAuthenticated
from apps.shared.paginations import CustomPageNumberPagination
from apps.shops.models import Cart, CartItem
from apps.shops.models import Watches, CustomWatch
from apps.shops.serializers import WatchListSerializer, CustomWatchSerializer, \
    AddCartItemSerializer, CartSerializer


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
        # Get or create a cart for the authenticated user
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

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


