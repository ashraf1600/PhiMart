from rest_framework.pagination import PageNumberPagination




class DefaultPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    