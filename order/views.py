from rest_framework.viewsets import GenericViewSet , ModelViewSet
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin , DestroyModelMixin
from .models import Cart , CartItem, Order
from .serializers import CartSerializer , CartItemSerializer , AddCartItemSerializer, CreateOrderSerializer, OrderSerializer ,UpdateCartitemSerializer, UpdateOrderSerializer , UpdateSerializer
from rest_framework.permissions import IsAuthenticated



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


    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return super().get_permissions()


    def get_serializer_class(self):

        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id' : self.request.user.id , 'user' : self.request.user }


    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user = self.request.user)