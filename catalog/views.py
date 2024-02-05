from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, \
    DetailView

from catalog.forms import ProductForm, VersionForm, BlogForm, CategoryForm
from catalog.models import Product, Category, Blog, Version


class HomeView(TemplateView):
    template_name = 'catalog/home.html'
    extra_context = {
        'title': 'Главная'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Product.objects.all()
        return context_data


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    extra_context = {
        'title': 'Категории товаров'
    }


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:categories')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:categories')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('catalog:categories')


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_queryset(self):
        return super().get_queryset().filter(
            category_id=self.kwargs.get('pk'),
            owner=self.request.user
        )

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk
        context_data['title'] = f'{category_item}'.title()

        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:categories')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:category_product', args=[self.object.category.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product

    def get_success_url(self):
        return reverse('catalog:category_product', args=[self.object.category.pk])


@login_required
def contacts(request):
    context = {
        'title': 'Контакты',
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('feedback.txt', 'w') as f:
            f.write(f'User_name: {name}\nContact_number: {phone}\n"{message}"\n')

    return render(request, 'catalog/contacts.html', context)


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
    permission_required = 'catalog.view_blog'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_publish=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['object_list'] = Blog.objects.filter(is_publish=True)
        return context_data


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('catalog:blog')
    permission_required = 'catalog.add_blog'

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    permission_required = 'catalog.change_blog'

    def get_success_url(self):
        return reverse('catalog:article', args=[self.object.pk])


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    permission_required = 'catalog.delete_blog'
    success_url = reverse_lazy('catalog:blog')
