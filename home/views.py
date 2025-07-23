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

def facebook(request):
    return render(request, 'home/facebook.html', context={
        'title': 'Facebook',
        'page': 'facebook',
        'app': 'home',
    })

def instagram(request):
    return render(request, 'home/instagram.html', context={
        'title': 'Instagram',
        'page': 'instagram',
        'app': 'home',
    })

def twitter(request):
    return render(request, 'home/twitter.html', context={
        'title': 'Twitter',
        'page': 'twitter',
        'app': 'home',
    })

def linkedin(request):
    return render(request, 'home/linkedin.html', context={
        'title': 'LinkedIn',
        'page': 'linkedin',
        'app': 'home',
    })

def youtube(request):
    return render(request, 'home/youtube.html', context={
        'title': 'YouTube',
        'page': 'youtube',
        'app': 'home',
    })

def track(request):
    return render(request, 'home/track.html', context={
        'title': 'Track',
        'page': 'track',
        'app': 'home',
    })

def returns(request):
    return render(request, 'home/returns.html', context={
        'title': 'Returns',
        'page': 'returns',
        'app': 'home',
    })

def shipping(request):
    return render(request, 'home/shipping.html', context={
        'title': 'Shipping',
        'page': 'shipping',
        'app': 'home',
    })

def faqs(request):
    return render(request, 'home/faqs.html', context={
        'title': 'FAQs',
        'page': 'faqs',
        'app': 'home',
    })
