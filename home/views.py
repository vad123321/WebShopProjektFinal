from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html', context={
        'title': 'Index',
        'page': 'index',
        'app': 'home',
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
