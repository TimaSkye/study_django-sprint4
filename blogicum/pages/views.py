from django.shortcuts import render


def page_not_found(request, exception):
    """Функция рендера кастомной страницы ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Функция рендера кастомной страницы ошибки 403."""
    return render(request, 'pages/403csrf.html', status=403)


def internal_server_error(request):
    """Функция рендера кастомной страницы ошибки 500."""
    return render(request, 'pages/500.html', status=500)
