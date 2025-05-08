from django.contrib.auth import logout
from django.shortcuts import render


def logout_view(request):
    """
    Костыль, необходимый для корректной работы реализации
    выхода пользователя, с выполнением условия
    'Не вносите изменения в шаблоны: они полностью готовы к работе.'
    """
    logout(request)
    return render(request, 'registration/logged_out.html')
