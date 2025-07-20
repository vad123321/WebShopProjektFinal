from django.shortcuts import render
from django.http import JsonResponse
from .models import Order, Delivery
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


def ajax_cart(request):
    response = dict()
    response['message'] = 'Hello from server!'

    uid = request.GET['uid']
    pid = request.GET['pid']
    price = request.GET['price']

    response['uid'] = uid
    response['pid'] = pid
    response['price'] = price

    order = Order.objects.filter(user_id=uid, product_id=pid, notes='Awaiting confirmation').first()
    if order:
        order.quantity += 1
        order.amount = order.quantity * float(price)
        order.save()
    else:
        Order.objects.create(
            title=f'Order-{pid}/{uid}/{timezone.now()}',
            user_id=uid,
            product_id=pid,
            amount=float(price),
            notes='Awaiting confirmation',
            quantity=1
        )

    # 2 - Зчитуємо із бази список всіх замовлень даного користувача:
    # user_orders = Order.objects.filter(user_id=uid)
    user_orders = Order.objects.filter(user_id=uid, notes='Awaiting confirmation')

    # 3 -Обчислюємо загальну вартість всіх замовлень даного користувача:
    # amount = 0
    # for order in user_orders:
    #     amount += order.amount
    count = sum(order.quantity for order in user_orders)
    amount = sum(order.amount for order in user_orders)
    

    # 4 - Записуємо дані у відповідь сервера:
    # response['amount'] = amount
    # response['count'] = len(user_orders)
    response['amount'] = amount
    response['count'] = count

    # 5 - Відправляєм дані клієнту:
    return JsonResponse(response)

def ajax_cart_indicate(request):
    response = dict()
    uid = request.GET.get('uid')
    if not uid:
        return JsonResponse({'error': 'uid parameter is required'}, status=400)
    user_orders = Order.objects.filter(user_id=uid)
    amount = sum(float(order.amount) for order in user_orders if order.amount)
    count = sum(order.quantity for order in user_orders)
    response['amount'] = amount
    response['count'] = count
    return JsonResponse(response)
# def ajax_cart_indicate(request):
#     response = dict()
#     uid = request.GET['uid']
#     user_orders = Order.objects.filter(user_id=uid)
#     # ->
#     amount = 0
#     for order in user_orders:
#         amount += order.amount
#     # ->
#     response['amount'] = amount
#     response['count'] = len(user_orders)
#     return JsonResponse(response)


def index(request):
    return render(request, 'orders/index.html', context={
        'title': 'Cart management',
        'page': 'index',
        'app': 'orders',
        'user_orders': Order.objects.filter(user_id=request.user.id)
    })


def bill(request, sel_list: str):
    # ->
    sel_list_str = sel_list.split(',')
    sel_list_num = [int(x) for x in sel_list_str[:-1]]
    total_price = int(sel_list_str[-1])
    final_list = []
    # ->
    for order_id in sel_list_num:
        order = Order.objects.get(id=order_id)
        final_list.append({
            'product_name': order.product.name,
            'category_name': order.product.category.name,
            'product_price': order.product.price,
            'product_photo': order.product.photo
        })
    # ->
    return render(request, 'orders/bill.html', context={
        'title': 'Order page',
        'page': 'bill',
        'app': 'orders',
        'total_price': total_price,
        'final_list': final_list,
        'init_list': sel_list
    })


def confirm(request, init_list: str):
    if request.method == 'GET':
        return render(request, 'orders/confirm.html', context={
            'title': 'Confirmation of order',
            'page': 'confirm',
            'app': 'orders',
            'init_list': init_list,
        })
    elif request.method == 'POST':
        email = request.POST.get('email')
        address = request.POST.get('address')
        # ->
        sel_list_str = init_list.split(',')
        sel_list_num = [int(x) for x in sel_list_str[:-1]]
        total_price = int(sel_list_str[-1])
        info_list = []
        # ->
        for order_id in sel_list_num:
            try:
                order = Order.objects.get(id=order_id)
                Delivery.objects.create(
                    order=order,
                    user=order.user,
                    product=order.product,
                    quantity=order.quantity,
                    amount=order.amount,
                    email=email,
                    address=address,
                    status='Awaiting shipment'
                )
                order.delete()  # Видаляємо з кошика
            except Order.DoesNotExist:
                continue
        # for order_id in sel_list_num:
        #     order = Order.objects.get(id=order_id)
        #     info_list.append({
        #         'product_name': order.product.name,
        #         'category_name': order.product.category.name,
        #         'product_price': order.product.price
        #     })
        # ->
        subject = 'Order notification on WebShop site'
        body = f"""
            <h1>{subject}</h1>
            <hr />
            <h2 style="color: purple">You have confirmed the order for the</h2>
            <h3>
            <ol>
        """
        # ->
        for item in info_list:
            body += f"""
                <li>{item.get('product_name')} / {item.get('category_name')} - {item.get('product_price')} usd</li>
            """
        # ->
        body += f"""
            </ol>
            </h3>
            <hr />
            <h2>Total amount to pay: <span style="color: red">{total_price} usd</span></h2>
        """
        # ->
        success = send_mail(subject, '', 'web.shop@gmail.com', [email], fail_silently=False, html_message=body)
        if success:
            return render(request, 'orders/thanks.html', context={
                'title': 'Thank you for your order',
                'page': 'thanks',
                'app': 'orders',
                'email': email
            })
        # ->
        else:
            return render(request, 'orders/failed.html', context={
                'title': 'Mail sending error',
                'page': 'failed',
                'app': 'orders',
            })


@csrf_exempt
def delete_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('id')
        try:
            Order.objects.get(id=order_id).delete()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})


@csrf_exempt
def update_order_quantity(request):
    if request.method == 'POST':
        order_id = request.POST.get('id')
        quantity = int(request.POST.get('quantity'))
        try:
            order = Order.objects.get(id=order_id)
            order.quantity = quantity
            order.amount = quantity * float(order.product.price)
            order.save()
            return JsonResponse({'success': True, 'amount': order.amount})
        except Order.DoesNotExist:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})
