from django.urls import path

from .views import RegisterCreateAPIView, LoginAPIView, AddressListCreateAPIView, \
    AddressDestroyUpdateAPIView, CountryListAPIView

urlpatterns = [
    path('register/', RegisterCreateAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name = 'login' ),

    path('address/', AddressListCreateAPIView.as_view(), name = 'address'),
    path('address-update', AddressDestroyUpdateAPIView.as_view(), name='address_update'),
    path('country-list', CountryListAPIView.as_view(), name='country'),

    # path('activate/<uidb64>/<token>', ActivateUserView.as_view(), name='activate'),

    # path('wishlist/', WishlistAPIView.as_view(), name='wishlist'),





    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]