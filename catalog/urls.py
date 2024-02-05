from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import HomeView, contacts, ProductListView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CategoryListView, ProductDetailView, BlogListView, BlogDetailView, \
    BlogCreateView, BlogUpdateView, BlogDeleteView, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),

    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),

    path('product/<int:pk>/', ProductListView.as_view(), name='category_product'),
    path('product/view/<int:pk>/', ProductDetailView.as_view(), name='view_product'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/view/<int:pk>/', BlogDetailView.as_view(), name='article'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/update/<int:pk>/', BlogUpdateView.as_view(), name='article_update'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='article_delete'),
]
