from django.shortcuts import render
from .models import Category, Producer, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse


def index(request):
    # -> 1
    categories = Category.objects.all()
    producers = Producer.objects.all()
    products = Product.objects.all()
    search_query = request.GET.get('s')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # -> 2
    selected_category_id = request.GET.get('category')
    selected_producer_id = request.GET.get('producer')

    # -> 3
    if selected_category_id:
        products = products.filter(category_id=selected_category_id)
    if selected_producer_id:
        products = products.filter(producer_id=selected_producer_id)

    # -> 4 ...

    # -> 5 Pagination
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(products, page_size)
    page = request.GET.get('page')
    # -> 6
    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
    # -> 7
    return render(request, 'catalog/index.html', context={
        'title': 'Products',
        'page': 'index',
        'app': 'catalog',
        'categories': categories,
        'producers': producers,
        'products': products,
        'products': paginated_products,
        'selected_category_id': selected_category_id,
        'selected_producer_id': selected_producer_id,
    })

def ajax_search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)[:5]
    categories = Category.objects.filter(name__icontains=query)[:5]
    results_products = [{'id': p.id, 'name': p.name} for p in products]
    results_categories = [{'id': c.id, 'name': c.name} for c in categories]
    return JsonResponse({
        'products': results_products,
        'categories': results_categories
    })