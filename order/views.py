from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from .models import Cart, CartItem, Order
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, CreateOrderSerializer, OrderSerializer, UpdateCartitemSerializer, UpdateOrderSerializer, EmptySerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import OrderService
from order import serializers as Ordersz
from django.shortcuts import get_object_or_404


# Create your views here.

class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Check if user already has a cart
        cart = Cart.objects.filter(user=request.user).first()
        
        if cart:
            # Return existing cart instead of creating new one
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        else:
            # Create new cart
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Cart.objects.filter(user_id=self.request.user.id)
    
    def list(self, request, *args, **kwargs):
        # Return user's cart as a list (for frontend compatibility)
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset.first())
            return Response([serializer.data])
        return Response([])


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartitemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    def get_queryset(self):
        cart_id = self.kwargs.get('cart_pk')
        return CartItem.objects.filter(cart_id=cart_id, cart__user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # Ensure cart exists and belongs to the user
        cart_id = self.kwargs.get('cart_pk')
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)
        return super().create(request, *args, **kwargs)


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user=request.user)
        return Response({'message': 'order cancelled successfully'})

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = Ordersz.UpdateOrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'order status updated successfully'})

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        elif self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'cancel':
            return Ordersz.EmptySerializer
        if self.action == 'create':
            return Ordersz.CreateOrderSerializer
        elif self.action == 'update_status':
            return Ordersz.UpdateOrderSerializer
        return Ordersz.OrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'user': self.request.user}

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)