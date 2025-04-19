from rest_framework import serializers
from .models import Category, Food, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class FoodSerializer(serializers.ModelSerializer):
    category_string = serializers.StringRelatedField(source='category', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    category_link = serializers.HyperlinkedRelatedField(source='category', view_name='category-detail', read_only=True)
    category_slug = serializers.SlugRelatedField(source='category', slug_field='name', read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'category', 'category_id', 'category_string', 'category_link', 'category_slug', 'price', 'description', 'available']

    def create(self, validated_data):
        return Food.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.available = validated_data.get('available', instance.available)
        instance.save()
        return instance

class OrderSerializer(serializers.ModelSerializer):
    food_string = serializers.StringRelatedField(source='food', read_only=True)
    food_id = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all(), source='food', write_only=True)
    food_link = serializers.HyperlinkedRelatedField(source='food', view_name='food-detail', read_only=True)
    food_slug = serializers.SlugRelatedField(source='food', slug_field='name', read_only=True)
    order_url = serializers.HyperlinkedIdentityField(view_name='order-detail', read_only=True)
    food = FoodSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'food', 'food_id', 'food_string', 'food_link', 'food_slug', 'quantity', 'total_price', 'created_at', 'order_url']

    def create(self, validated_data):
        food = validated_data['food']
        quantity = validated_data['quantity']
        total_price = food.price * quantity
        return Order.objects.create(
            user=self.context['request'].user,
            food=food,
            quantity=quantity,
            total_price=total_price
        )

    def update(self, instance, validated_data):
        instance.food = validated_data.get('food', instance.food)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        if 'quantity' in validated_data:
            instance.total_price = instance.food.price * validated_data['quantity']
        instance.save()
        return instance