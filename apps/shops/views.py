from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.shared.authenticated import CustomIsAuthenticated
from apps.shared.paginations import CustomPageNumberPagination
from apps.shops.models import Watches, CustomWatch
from apps.shops.serializers import WatchListSerializer, CustomWatchSerializer


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
    permission_classes = [CustomIsAuthenticated,]

