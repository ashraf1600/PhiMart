from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category , Review
from product.serializers import ProductSerializer, CategorySerializer , ReviewSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter , OrderingFilter
from product.paginations import DefaultPagination

'''
| বিষয়               | কাজ                                                                       
| ------------------ | ------------------------------------------------------------------------- 
| `ModelViewSet`     | Create, Read, Update, Delete সব একসাথে করতে দেয়                          
| `serializer_class` | মডেল থেকে JSON ও JSON থেকে মডেল এ রূপান্তর করে                            
| `queryset`         | কোন কোন ডেটা কাজ করবে সেটা নির্ধারণ করে                                   
| `destroy()`        | প্রোডাক্ট ডিলিট করার সময় কাস্টম চেক করা হয় (স্টক ১০ এর বেশি হলে ডিলিট না) 

'''





class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend , OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    pagination_class =DefaultPagination
    search_fields = ['name', 'description' ] 
    ordering_fields = ['price','updated_at']

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response({'message': "Product with stock more than 10 can't be deleted"})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):  # Typo fixed here
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        return Review.objects.filter(product_id=product_id)

    def get_serializer_context(self): 
        return {'product_id': self.kwargs['product_pk']}

    def perform_create(self, serializer):
        product_id = self.kwargs['product_pk']

        # 🛠 Capital 'P' for Product (model class)
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            raise NotFound("Product not found")

        serializer.save(product=product)

    
