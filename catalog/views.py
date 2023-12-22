from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('feedback.txt', 'w') as f:
            f.write(f'{name} - {phone}, ({message})')

    return render(request, 'contacts/contacts.html')
