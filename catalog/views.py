from django.shortcuts import render

from catalog.models import Product


# Create your views here.
def home(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Главная'
    }
    return render(request, 'catalog/home.html', context)


def prod(request, pk):
    prod_item = Product.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(id=pk),
        'title': f'{prod_item.product_name}',
    }
    return render(request, 'catalog/prod.html', context)


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
