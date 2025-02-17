from django.urls import path
from products import views


urlpatterns = [
    path('list/', views.ProductsListView.as_view(), name='product-list'),
]