from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from catalog.models import Product
from .models import Favorite

from django.contrib import messages
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .utils import send_verification_email, check_verification_token


def signup(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html', context={
            'title': 'Реєстрація',
            'page': 'signup',
            'app': 'accounts'
        })
    elif request.method == 'POST':
        # 1 - Отримуємо дані із форми:
        login_x = request.POST.get('username')
        pass1_x = request.POST.get('pass1')
        pass2_x = request.POST.get('pass2')
        email_x = request.POST.get('email')

        # 2 - Додаємо користувача в базу:
        user = User.objects.create_user(login_x, email_x, pass1_x)

        # 3 - Формуємо звіт:
        if user is None:
            color = 'red'
            message = 'Не вдалось зберегти дані користувача в базі'
        else:
            user.is_active = False # Deactivate the user until email confirmation
            user.save()
            send_verification_email(request, user)

            color = 'green'
            message = 'User registered successfully! Please check your email to confirm your account.'
            
        return render(request, 'accounts/report.html', context={
            'title': 'Звіт про реєстрацію',
            'page': 'report',
            'app': 'accounts',
            'color': color,
            'message': message
        }) 


def signin(request):
    if request.method == 'GET':
        return render(request, 'accounts/signin.html', context={
            'title': 'Авторизація',
            'page': 'signin',
            'app': 'accounts'
        })
    elif request.method == 'POST':
        login_x = request.POST.get('username')
        pass1_x = request.POST.get('pass1')

        user = authenticate(request, username=login_x, password=pass1_x)

        if user is not None:
            login(request, user)
            color = 'green'
            message = 'Login successful!'
        
        else:
            try:
                potential_user = User.objects.get(username=login_x)
            except User.DoesNotExist:
                potential_user = None

            if potential_user is not None and not potential_user.is_active:
                color = 'red'
                message = 'Your account is not active. Please check your email for the activation link.'
            else:
                color = 'red'
                message = 'User not found'

        return render(request, 'accounts/report.html', context={
            'title': 'Звіт про авторизацію',
            'page': 'report',
            'app': 'accounts',
            'color': color,
            'message': message
        })


def signout(request):
    logout(request)
    return render(request, 'accounts/signout.html', context={
        'title': 'Вихід',
        'page': 'signout',
        'app': 'accounts'
    })


def profile(request):
    # ...
    return render(request, 'accounts/profile.html', context={
        'title': 'Профіль',
        'page': 'profile',
        'app': 'accounts'
    })


def ajaxreg(request):
    response = dict()
    login_y = request.GET.get('username')
    # ->
    try:
        User.objects.get(username=login_y)
        response['message'] = 'Логін - зайнятий!'
    except User.DoesNotExist:
        response['message'] = 'Логін - вільний!'
    # ->
    return JsonResponse(response)


@login_required
def favorites(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        Favorite.objects.get_or_create(user=request.user, product=product)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    fav_products = Product.objects.filter(favorited_by__user=request.user)
    return render(request, 'accounts/favorites.html', {'favorites': fav_products})


def activate(request, uidb64, token):
    """ 
    Activate user account after email verification.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # ->
    if user is not None and check_verification_token(user, token):
        user.is_active = True
        user.save()
        message = 'Your account has been successfully activated!'
        color = 'green'
    else:
        message = 'Activation link is invalid or has expired.'
        color = 'red'

    return render(request, 'accounts/report.html', context={
            'title': 'Activation Report',
            'page': 'report',
            'app': 'accounts',
            'color': color,
            'message': message
        }) 


@login_required
def remove_favorite(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        favorite = Favorite.objects.filter(user=request.user, product_id=product_id)
        favorite.delete()
    return redirect(request.META.get('HTTP_REFERER', '/')) 


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        user = request.user

        if not user.check_password(old_password):
            message = 'Current password is incorrect.'
            color = 'red'
        elif new_password1 != new_password2:
            message = 'New passwords do not match.'
            color = 'red'
        elif len(new_password1) < 6:
            message = 'New password must be at least 6 characters.'
            color = 'red'
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            message = 'Password changed successfully!'
            color = 'green'
        return render(request, 'accounts/report.html', {
            'title': 'Change Password',
            'color': color,
            'message': message,
            'page': 'report',
            'app': 'accounts'
        })
    return render(request, 'accounts/change_password.html', {
        'title': 'Change Password',
        'page': 'change_password',
        'app': 'accounts'
    })
