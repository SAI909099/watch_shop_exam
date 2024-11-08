from django.urls import include
from django.urls import path

urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('shops/', include('apps.shops.urls')),

]
