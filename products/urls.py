from django.urls import path, include
from .views import (
        ProductListCreateView, 
        ProductDetailView, 
        ProductViewSet, 
        CategoryViewSet, 
        ProductImageUploadView,
        ReviewListCreateView, 
        ReviewUpdateDeleteView,
        WishlistListView,
        WishlistAddView,
        WishlistRemoveView,
        )
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
        path('', include(router.urls)),
        path('', ProductListCreateView.as_view(), name='product-list'),
        path('<int:pk>', ProductDetailView.as_view(), name='product-detail'),
        path('products/<int:product_id>/images/', ProductImageUploadView.as_view(), name='product-image-upload'),
        path('products/<int:product_id>/reviews/', ReviewListCreateView.as_view(), name='product-reviews'),
        path('reviews/<int:pk>/', ReviewUpdateDeleteView.as_view(), name='review-detail'),
        path('wishlist/', WishlistListView.as_view(), name='wishlist-list'),
        path('wishlist/add/', WishlistAddView.as_view(), name='wishlist-add'),
        path('wishlist/<int:pk>/remove', WishlistRemoveView.as_view(), name='wishlist-remove'),
        ]

