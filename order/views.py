from rest_framework.viewsets import GenericViewSet , ModelViewSet
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin , DestroyModelMixin
from .models import Cart , CartItem
from .serializers import CartSerializer , CartItemSerializer , AddCartItemSerializer ,UpdateCartitemSerializer


# Create your views here.

class CartViewSet(CreateModelMixin, GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = CartSerializer

   
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
        return CartItem.objects.filter(cart_id = self.kwargs['cart_pk'])