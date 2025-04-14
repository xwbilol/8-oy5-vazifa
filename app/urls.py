from django.urls import path
from .views import (
    CategoryListCreateView, CategoryRetrieveUpdateDestroyView,
    FoodListCreateView, FoodRetrieveUpdateDestroyView,
    OrderListCreateView, OrderRetrieveUpdateDestroyView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('foods/', FoodListCreateView.as_view(), name='food-list'),
    path('foods/<int:pk>/', FoodRetrieveUpdateDestroyView.as_view(), name='food-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),

]