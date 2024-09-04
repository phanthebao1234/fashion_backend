# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CaterogyList.as_view(), name='category-list'),
    path('categories/home', views.HomeCaterogyList.as_view(), name='home-category-list'),
    path('brands/', views.BrandList.as_view(), name='brand-list'),
    path('', views.ProductList.as_view(), name='product-list'),
    path('popular/', views.PopularProductList.as_view(), name='popular-product'),
    path('byType/', views.PopularProductListByClothesType.as_view(), name='list-by-type'),
    path('search/', views.SearchProductByTitle.as_view(), name='search'),
    path('recommendations/', views.SimilarProduct.as_view(), name='similar-products'),
    path('category/', views.FilterProductByCategory.as_view(), name='product-by-category'),
]
