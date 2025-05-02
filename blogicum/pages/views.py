from django.shortcuts import render


def about(request):
    """Фунцкия рендера страницы о проекте."""
    return render(request, 'pages/about.html')


def rules(request):
    """Фунцкия рендера страницы правил."""
    return render(request, 'pages/rules.html')
