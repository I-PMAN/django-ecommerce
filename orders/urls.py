from django.urls import path, include
from .views import (
        CartView,
        AddToCartView,
        UpdateCartItemView,
        PaymentSimulationView,
        OrderViewSet,
        CheckoutView,
        AddressListCreateView,
        AddressUpdateDeleteView,
        SetDefaultAddressView,
        )
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
        path('', include(router.urls)),
        path('cart/', CartView.as_view(), name='cart-detail'),
        path('cart/add', AddToCartView.as_view(), name='cart-add'),
        path('cart/item/<int:pk>', UpdateCartItemView.as_view(), name='cart-item-update'),
        path('checkout/', CheckoutView.as_view(), name='checkout'),
        path('orders/<int:pk>/pay/', PaymentSimulationView.as_view(), name='order-pay'),
        path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
        path('addresses/<int:pk>/', AddressUpdateDeleteView.as_view(), name='address-update-delete'),
        path('addresses/<int:pk>/set-default/', SetDefaultAddressView.as_view(), name='set-default-address'),
        ]


