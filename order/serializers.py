from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from product.serializers import ProductSerializer
from product.models import Product
from django.db import models

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id','product_id' , 'quantity']


    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id , product_id=product_id )
            cart_item.quantity +=quantity

            self.instance = cart_item.save() 

        except cart_item.DoesNotExist:
           
           self.instance = CartItem.objects.create(cart_id = cart_id , **self.validated_data )   

        return self.instance 
    
    def validate_product_id(self , value ):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                f"Product with id {value} does not exists")
        return value
      

class UpdateCartitemSerializer(serializers.ModelSerializer):
    class Meta :
        model = CartItem
        fields = ['quantity']
        
             





    



class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
   
    class Meta:
        model = CartItem
        fields = ['id','product', 'quantity',]

    def get_total_price(self , cart_item:CartItem):
        return cart_item.quantity * cart_item.product.price   



class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True , read_only = True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'user','items','total_price']
        read_only_fields = ['user']

    def get_total_price(self , cart:Cart):

        return sum( [ item.product.price * item.quantity for item in cart.items.all()])

class CreateOrderSerializer(serializers.Serializer):

    cart_id = serializers.UUIDField()


    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the given id was found')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty')
        return cart_id

    def create(self, validated_data):
        user_id = self.context['user_id']  
        cart_id = validated_data['cart_id']  
        cart = Cart.objects.get(pk=cart_id)
        cart_items = cart.select_related('product').all()

        total_price = sum([item.quantity * item.product.price for item in cart_items])
        order = Order.objects.create(user_id=user_id, total_price=total_price)
        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                total_price=item.quantity * item.product.price
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)
        cart_items.delete()
        return order
    
    def to_representation(self, instance):
        return OrderSerializer(instance).data
    

### test




class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','order','product','quantity','price','total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','user','status','total_price','created_at','items']



   