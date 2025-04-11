from rest_framework.throttling import UserRateThrottle

class CategoryThrottle(UserRateThrottle):
    scope = 'category'
    rate = '10/minute'

class FoodThrottle(UserRateThrottle):
    scope = 'food'
    rate = '15/minute'

class OrderThrottle(UserRateThrottle):
    scope = 'order'
    rate = '5/minute'