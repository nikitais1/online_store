from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_of_views += 1
        self.object.save()
        if self.object.count_of_views == 100:
            send_mail(subject="hi there", message="good job", from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[settings.EMAIL_HOST_USER])

        return self.object


class BlogListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Blog
    permission_required = 'blog.view_blog'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_publish=True)
        return queryset


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog')
    permission_required = 'blog.add_blog'

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    permission_required = 'blog.change_blog'

    def get_success_url(self):
        return reverse('blog:article', args=[self.object.pk])


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    permission_required = 'blog.delete_blog'
    success_url = reverse_lazy('blog:blog')
