from django.urls import path
from . import views

urlpatterns = [
    path('', views.categoryList.as_view(), name='view_categories'),
    path('<int:pk>/', views.categoryDetail.as_view(), name='view_specific_category'),
]