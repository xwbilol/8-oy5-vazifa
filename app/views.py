from rest_framework import generics
from .models import Category, Food, Order
from .serializers import CategorySerializer, FoodSerializer, OrderSerializer
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

    def perform_create(self, serializer):
        food = serializer.validated_data['food']
        quantity = serializer.validated_data['quantity']
        total_price = food.price * quantity
        serializer.save(user=self.request.user, total_price=total_price)

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdmin]
    throttle_classes = [OrderThrottle]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)