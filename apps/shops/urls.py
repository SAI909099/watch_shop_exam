

from django.urls import path

from apps.shops.views import WatchListApiView, CustomWatchCreateApiView, CartView, AddToCartView, \
    UpdateCartItemView, RemoveCartItemView, OrderView, OrderDetailView

urlpatterns = [

    path('wath-list/', WatchListApiView.as_view(), name='wath_list'),
    path('custom-watch/', CustomWatchCreateApiView.as_view(), name='custom_watch'),

    path('cart/', CartView.as_view(), name='cart-detail'),  # Retrieve the current user's cart
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),  # Add an item to the cart
    path('cart/item/<int:pk>/', UpdateCartItemView.as_view(), name='update-cart-item'),  # Update cart item quantity
    path('cart/item/<int:pk>/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),  # Remove a cart item

    path('api/v1/shops/order/', OrderView.as_view(), name='order'),
    path('api/v1/shops/order/<int:id>/', OrderDetailView.as_view(), name='order-detail'),

]
