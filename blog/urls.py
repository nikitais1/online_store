from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, \
    BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/view/<int:pk>/', BlogDetailView.as_view(), name='article'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/update/<int:pk>/', BlogUpdateView.as_view(), name='article_update'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='article_delete'),
]
