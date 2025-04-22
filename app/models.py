from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='student')

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    price = models.IntegerField()
    description = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    experience = models.IntegerField()
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Teacher: {self.user.username}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    course = models.IntegerField()
    group = models.CharField(max_length=10)

    def __str__(self):
        return f"Student: {self.user.username}"