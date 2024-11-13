from django.urls import path

from apps.shops.views import WatchListApiView, CustomWatchCreateApiView

urlpatterns = [
    path('wath-list/', WatchListApiView.as_view(), name='wath_list'),
    path('custom-watch/', CustomWatchCreateApiView.as_view(), name='custom_watch'),
]