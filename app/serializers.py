from rest_framework import serializers
from .models import Category, Food, Order, User, Teacher, Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'experience', 'specialization']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'teacher'
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'course', 'group']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'student'
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        student = Student.objects.create(user=user, **validated_data)
        return student

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
    category = CategorySerializer()

    class Meta:
        model = Food
        fields = ['id', 'name', 'category', 'price', 'description', 'available']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category_serializer = CategorySerializer(data=category_data)
        category_serializer.is_valid(raise_exception=True)
        category = category_serializer.save()
        food = Food.objects.create(category=category, **validated_data)
        return food

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        if category_data:
            category_serializer = CategorySerializer(instance.category, data=category_data, partial=True)
            category_serializer.is_valid(raise_exception=True)
            category_serializer.save()
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.available = validated_data.get('available', instance.available)
        instance.save()
        return instance

class OrderSerializer(serializers.ModelSerializer):
    food = FoodSerializer()
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'food', 'quantity', 'total_price', 'created_at']

    def create(self, validated_data):
        food_data = validated_data.pop('food')
        food_serializer = FoodSerializer(data=food_data)
        food_serializer.is_valid(raise_exception=True)
        food = food_serializer.save()
        quantity = validated_data['quantity']
        total_price = food.price * quantity
        order = Order.objects.create(
            user=self.context['request'].user,
            food=food,
            quantity=quantity,
            total_price=total_price
        )
        return order

    def update(self, instance, validated_data):
        food_data = validated_data.pop('food', None)
        if food_data:
            food_serializer = FoodSerializer(instance.food, data=food_data, partial=True)
            food_serializer.is_valid(raise_exception=True)
            food_serializer.save()
        instance.quantity = validated_data.get('quantity', instance.quantity)
        if 'quantity' in validated_data:
            instance.total_price = instance.food.price * validated_data['quantity']
        instance.save()
        return instance