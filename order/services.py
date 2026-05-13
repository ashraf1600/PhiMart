from order.models import Order, OrderItem , Cart , CartItem
from django.db import transaction



class OrderService:
    @staticmethod

    def create_order(user_id, cart_id):
        with transaction.atomic():
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
        # Logic to create an order
        