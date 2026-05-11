from django.db import models
from users.models import User  # Assuming you have a User model in users app
from product.models import Product  # Assuming you have a Product model in product app
from uuid import uuid4
from django.core.validators import MinValueValidator

# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4 , editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.first_name} created at {self.created_at}"



class CartItem(models.Model): # done
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming Product model exists in product app
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])


    class Meta:
        unique_together = [['cart', 'product']]
  

    def __str__(self):
        return f"{self.quantity} X {self.product.name} in cart of {self.cart.user.first_name}"


class Order(models.Model):

    NOT_PAID = 'Not Paid'
    READY_TO_SHIP = 'Ready to Ship'
    SHIPPED = 'Shipped'
    DELIVERD = 'Delivered'
    CANCELED = 'Canceled'
    STATUS_CHOICES = [
        (NOT_PAID, 'Not Paid'),
        (READY_TO_SHIP, 'Ready to Ship'),
        (SHIPPED, 'Shipped'),
        (DELIVERD, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_PAID)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

    def __str__(self):
        return f"Order {self.id} by {self.user.username} on {self.created_at} with status {self.status}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming Product model exists in product app
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity} X {self.product.name} in order {self.order.id}"