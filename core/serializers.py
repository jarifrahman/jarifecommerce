from rest_framework import serializers
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon, Refund, Category, Video, ProductHit






class ItemSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    class Meta:
        model = Item
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = "__all__"

class ProducthitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductHit
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id','name','videofile', 'category')