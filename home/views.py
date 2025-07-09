from django.shortcuts import render
from catalog.models import Product

def index(request):
    mobile_products = Product.objects.filter(category__id=2)[:4]
    smart_watches = Product.objects.filter(category__id=3)[:4]

    return render(request, 'home/index.html', context={
        'title': 'Index',
        'page': 'index',
        'app': 'home',
        'mobile_products': mobile_products,
        'smart_watches': smart_watches,
    })

def about(request):
    return render(request, 'home/about.html', context={
        'title': 'About',
        'page': 'about',
        'app': 'home',
    })

def contacts(request):
    return render(request, 'home/contacts.html', context={
        'title': 'Contacts',
        'page': 'contacts',
        'app': 'home',
    })

def services(request):
    return render(request, 'home/services.html', context={
        'title': 'Services',
        'page': 'services',
        'app': 'home',
    })

def blog(request):
    return render(request, 'home/blog.html', context={
        'title': 'Blog',
        'page': 'blog',
        'app': 'home',
    })
