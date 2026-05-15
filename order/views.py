from rest_framework.viewsets import GenericViewSet , ModelViewSet
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin , DestroyModelMixin
from .models import Cart , CartItem, Order
from .serializers import CartSerializer , CartItemSerializer , AddCartItemSerializer, CreateOrderSerializer, OrderSerializer ,UpdateCartitemSerializer, UpdateOrderSerializer , EmptySerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import OrderService
from order import serializers as Ordersz



# Create your views here.

class CartViewSet(CreateModelMixin, GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    # queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


    def get_queryset(self):
        return Cart.objects.filter(user_id = self.request.user.id)

   
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get' , 'post' , 'patch' , 'delete']

    def get_serializer_class(self):
        if self.request.method =='POST':
            return AddCartItemSerializer
        elif self.request == 'PATCH':
            return UpdateCartitemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id' : self.kwargs['cart_pk']}
    
       

    def get_queryset(self):
        return CartItem.objects.prefetch_related('items__product').filter(user = self.request.user)
    





class OrderViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get' , 'post' , 'patch', 'delete', 'head', 'options']
    @action(methods = ['post'] , detail = True, permission_classes=[IsAuthenticated])
    def cancel(self , request , pk = None):

        order = self.get_object()
        OrderService.cancel_order(order=order , user = request.user)
        return Response({'message' : 'order cancelled successfully'})


    @action(methods = ['post'] , detail = True, permission_classes=[IsAuthenticated]) 

    def update_status(self , request , pk = None):

        order = self.get_object()
        serializer = Ordersz.UpdateOrderSerializer(order , data = request.data,partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message' : 'order status updated successfully'})
        


    def get_permissions(self):
        if self.action in ['update_status' , 'destroy']:
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
        return {'user_id' : self.request.user.id , 'user' : self.request.user }


    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user = self.request.user)