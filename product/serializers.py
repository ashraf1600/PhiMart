from rest_framework import serializers
from decimal import Decimal
from product.models import Product, Category, ProductImage, Review
from django.contrib.auth import get_user_model


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url']
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    price_with_tax = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'category_name', 'price_with_tax', 'main_image', 'images', 'created_at']

    def get_price_with_tax(self, product):
        return round(product.price * Decimal(1.1), 2)
    
    def get_main_image(self, obj):
        request = self.context.get('request')
        # First try to get from ProductImage
        first_image = obj.images.first()  # Using related_name='images'
        if first_image and first_image.image:
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        
        # Fallback to main product image field
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_images(self, obj):
        request = self.context.get('request')
        images = obj.images.all()
        if images:
            image_urls = []
            for img in images:
                if img.image:
                    if request:
                        image_urls.append(request.build_absolute_uri(img.image.url))
                    else:
                        image_urls.append(img.image.url)
            return image_urls
        return []


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'name', 'email']

    def get_name(self, obj):
        return obj.get_full_name() or obj.email


class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'ratings', 'comment', 'created_at']
        read_only_fields = ['user', 'product', 'created_at']

    def create(self, validated_data):
        user = self.context.get('request').user
        product_id = self.context.get('product_id')
        # Remove any user key if present (shouldn't be)
        validated_data.pop('user', None)
        return Review.objects.create(
            product_id=product_id,
            user=user,
            **validated_data
        )