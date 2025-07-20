from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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
            user.save()
            color = 'green'
            message = 'Реєстрація успішно завершена!'
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
        # 1 - Отримуємо дані із форми:
        login_x = request.POST.get('username')
        pass1_x = request.POST.get('pass1')

        # 2 - Перевіряємо чи є такий користувач в БД:
        user = authenticate(request, username=login_x, password=pass1_x)

        # 3 - Формуємо негативний звіт:
        if user is None:
            color = 'red'
            message = 'Користувач не знайдений'
        
        # 4 - Формуємо позитивний звіт:
        else:
            login(request, user)
            color = 'green'
            message = 'Авторизація успішно!'

        # 5 - Завантаження сторінки звіту:
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
