from django.urls import path

from products.viewsets import ProductViewSet, UserAPIView

urlpatterns = [
    path('products', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='product-list'),

    path('products/<str:pk>', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='product-detail'),

    path('user', UserAPIView.as_view(), name='user-detail'),
]
