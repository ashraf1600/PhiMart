from rest_framework import serializers
from decimal import Decimal
from product.models import Product , Category , Review



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']

    product_count = serializers.SerializerMethodField(method_name='get_product_count')

    def get_product_count(self, category):
        count = Product.objects.filter(category=category).count()  
        return count
        
    
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),  # এখানে অবশ্যই Category মডেল হতে হবে
        view_name='category-detail',

    )
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'price_with_tax']

    def get_price_with_tax(self, product):
        return round(product.price * Decimal(1.1), 2)  # Assuming 10% tax rate
    
    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return price


class ReviewSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Review
        fields = ['id', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context.get('product_id')
        return Review.objects.create(product_id=product_id, **validated_data)    


           