from rest_framework import generics
from .models import Category, Food, Order
from .serializers import CategorySerializer, FoodSerializer, OrderSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class FoodListCreateView(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAdminOrReadOnly]

class FoodRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAdminOrReadOnly]

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdmin]

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

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)