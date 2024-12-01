from django.urls import path

from .views import AddressListCreateAPIView, \
    AddressDestroyUpdateAPIView, CountryListAPIView, UserInfoListCreateAPIView, \
    PasswordResetConfirmView, ActivateUserView, ShippingMethodListView, \
    ValidateCardAPIView, ContactAPIView, ResetPasswordAPIView, ForgetPasswordAPIView, VerifyEmailAPIView, \
    RegisterAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    # path('login/', LoginAPIView.as_view(), name='login'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('login/' ,LoginAPIView.as_view(), name='login'),
    path('user-detail/', UserInfoListCreateAPIView.as_view(), name='user-detail' ),

    path('address/', AddressListCreateAPIView.as_view(), name = 'address'),
    path('address-update/<int:pk>', AddressDestroyUpdateAPIView.as_view(), name='address_update'),
    path('country-list', CountryListAPIView.as_view(), name='country'),

    # path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', PasswordResetConfirmView.as_view(), name='reset-password'),

    path('activate/<uidb64>/<token>', ActivateUserView.as_view(), name='activate'),

    path('shipping-methods/', ShippingMethodListView.as_view(), name='shipping-methods'),

    path('validate-card/', ValidateCardAPIView.as_view(), name='validate-card'),

    path('contact/', ContactAPIView.as_view(),name='contact-us'),

    path('forget-password/', ForgetPasswordAPIView.as_view(), name='forget-password'),
    # path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/<int:uid>/<str:token>/', ResetPasswordAPIView.as_view(), name='reset-password'),

    # path('wishlist/', WishlistAPIView.as_view(), name='wishlist'),





    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]