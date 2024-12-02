

from django.urls import path

from apps.shops.views import WatchListApiView, CustomWatchCreateApiView, CartView, AddToCartView, \
    UpdateCartItemView, RemoveCartItemView, WatchDetailListAPIView

urlpatterns = [

    path('wath-list/', WatchListApiView.as_view(), name='wath_list'),
    path('custom-watch/', CustomWatchCreateApiView.as_view(), name='custom_watch'),
    path('Watch-detail/<int:pk>/', WatchDetailListAPIView.as_view(), name='watch_detail'),

    path('cart/', CartView.as_view(), name='cart-detail'),  # Retrieve the current user's cart
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),  # Add an item to the cart
    path('cart/item/<int:pk>/', UpdateCartItemView.as_view(), name='update-cart-item'),  # Update cart item quantity
    path('cart/item/<int:pk>/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),  # Remove a cart item

]
