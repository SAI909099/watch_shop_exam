from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterCreateAPIView, LoginAPIView, ActivateUserView, WishlistAPIView, AddressListCreateAPIView

urlpatterns = [
    path('register/', RegisterCreateAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name = 'login' ),

    path('address/', AddressListCreateAPIView.as_view()),

    path('activate/<uidb64>/<token>', ActivateUserView.as_view(), name='activate'),

    path('wishlist/', WishlistAPIView.as_view(), name='wishlist'),





    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]