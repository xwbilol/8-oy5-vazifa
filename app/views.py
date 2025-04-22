from rest_framework import generics
from .models import Category, Food, Order, Teacher, Student
from .serializers import (
    CategorySerializer, FoodSerializer, OrderSerializer,
    TeacherSerializer, StudentSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .throttles import CategoryThrottle, FoodThrottle, OrderThrottle
from .pagination import CustomPagination

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [CategoryThrottle]
    pagination_class = CustomPagination

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [CategoryThrottle]

class FoodListCreateView(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [FoodThrottle]
    pagination_class = CustomPagination

class FoodRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [FoodThrottle]

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdmin]
    throttle_classes = [OrderThrottle]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdmin]
    throttle_classes = [OrderThrottle]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class TeacherCreateView(generics.CreateAPIView):
    serializer_class = TeacherSerializer

class StudentCreateView(generics.CreateAPIView):
    serializer_class = StudentSerializer