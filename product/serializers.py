from rest_framework import serializers
from decimal import Decimal
from product.models import Product , Category, ProductImage , Review
from django.contrib.auth import get_user_model




class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [ 'id', 'image']        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']

    product_count = serializers.SerializerMethodField(method_name='get_product_count')

    def get_product_count(self, category):
        count = Product.objects.filter(category=category).count()  
        return count
        
    
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)


    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),  # এখানে অবশ্যই Category মডেল হতে হবে
        view_name='category-detail',

    )
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'price_with_tax', 'images']

    def get_price_with_tax(self, product):
        return round(product.price * Decimal(1.1), 2)  # Assuming 10% tax rate
    
    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return price


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

        def get_current_user_name(self, obj):

            return obj.get_full_name()

class ReviewSerializer(serializers.ModelSerializer): 
    # user = SimpleUserSerializer()  # রিভিউ লেখার সময় ইউজার ফিল্ডটি read-only করা হয়েছে
    user = serializers.SerializerMethodField(method_name='get_user')  # রিভিউ লেখার সময় ইউজার ফিল্ডটি read-only করা হয়েছে
    class Meta:
        model = Review
        fields = ['id', 'user','product','ratings', 'comment']
        read_only_fields = ['user', 'product']  # user এবং product ফিল্ডগুলো read-only করা হয়েছে

        def get_user(self, obj):
            return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        product_id = self.context.get('product_id')
        return Review.objects.create(product_id=product_id, **validated_data)






           