from django_filters.rest_framework import FilterSet
from product.models import Product, Category


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category_id': ['exact'],
            'price': [ 'lt', 'gt'],
        }