from django.urls import path
from products import views


urlpatterns = [
    path('list/', views.ProductsListView.as_view(), name='product-list'),
    path('detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('category/', views.CategoriesListView.as_view(), name='category'),
    path('like/<slug:product_slug>/', views.LikeProductView.as_view({'post': 'like_product'}), name='like-product'),
]