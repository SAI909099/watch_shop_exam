from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from apps.shops.models import Watches, CustomWatch
from apps.shops.serializers import WatchListSerializer, CustomWatchSerializer


@extend_schema(tags=['watch_list'])
class WatchListApiView(ListAPIView):
    queryset = Watches.objects.all()
    serializer_class = WatchListSerializer
    authentication_classes = AllowAny,


@extend_schema(tags=['custom_watch'])
class CustomWatchCreateApiView(CreateAPIView):
    queryset = CustomWatch.objects.all()
    serializer_class = CustomWatchSerializer
    permission_classes = AllowAny,
    authentication_classes = AllowAny,
