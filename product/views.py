from rest_framework.response import Response
from rest_framework import status
from api.permissions import IsAdminOrReadOnly
from product.models import Product, Category, ProductImage, Review
from product.serializers import ProductImageSerializer, ProductSerializer, CategorySerializer, ReviewSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from product.paginations import DefaultPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.permissions import DjangoModelPermissions
from product.permissions import IsReviewAuthorOrReadOnly


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        """Pass request to serializer for full image URLs"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response({'message': "Product with stock more than 10 can't be deleted"})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        """Pass request to serializer for full image URLs"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        product_id = self.kwargs['product_pk']
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            raise NotFound("Product not found")
        serializer.save(product=product)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        return Review.objects.filter(product_id=product_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product_id'] = self.kwargs['product_pk']
        context['request'] = self.request # kfnl
        return context

    def perform_create(self, serializer):
        product_id = self.kwargs['product_pk']
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            raise NotFound("Product not found")
        serializer.save(product=product, user=self.request.user)