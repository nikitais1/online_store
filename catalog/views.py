from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView

from catalog.forms import ProductForm, VersionForm, ModeratorProductForm
from catalog.models import Product, Category, Version


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class ProductListView(LoginRequiredMixin, ListView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

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

    def get_form_class(self):
        if self.request.user == self.object.owner:
            return ProductForm
        elif self.request.user.groups.filter(name='moderator'):
            return ModeratorProductForm
        else:
            raise Http404('Вы не являетесь владельцем данного товара')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')

    def get_object(self, queryset=None, *args, **kwargs):
        object_data = super().get_object(*args, **kwargs)
        if self.request.user == object_data.owner:
            return object_data
        else:
            raise Http404('Вы не являетесь владельцем данного товара')


class VersionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'catalog/product_form.html'
    model = Version
    form_class = VersionForm
    permission_required = 'catalog.add_version'
    success_url = reverse_lazy('catalog:index')


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
