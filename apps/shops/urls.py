

from django.urls import path

from apps.shops.views import WatchListApiView, CustomWatchCreateApiView, CartView, AddToCartView, \
    UpdateCartItemView, RemoveCartItemView, OrderView, OrderDetailView

urlpatterns = [

    path('wath-list/', WatchListApiView.as_view(), name='wath_list'),
    # path('custom-watch/', CustomWatchCreateApiView.as_view(), name='custom_watch'),

    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/item/<int:pk>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/item/<int:pk>/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),

    path('order/', OrderView.as_view(), name='order'),
    path('order/<int:id>/', OrderDetailView.as_view(), name='order-detail'),

]
