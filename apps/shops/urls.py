from django.urls import path
from apps.shops.views import ProductListAPIView

urlpatterns = [
    path('product/', ProductListAPIView.as_view()),
]
