from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('feedback.txt', 'w') as f:
            f.write(f'User_name: {name}\nContact_number: {phone}\n"{message}"\n')

    return render(request, 'catalog/contacts.html')
