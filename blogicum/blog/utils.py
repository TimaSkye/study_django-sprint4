from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse
from django.utils import timezone

from .constants import TRUNCATE_LENGTH


def truncate_text(text, truncate_length=TRUNCATE_LENGTH):
    """Функция обрезки строк."""
    if not text:
        return ''
    return (text[:truncate_length] + (
        '...' if len(text) > truncate_length else ''))


def get_filter_query(queryset, **kwargs):
    """фильтрация по 'опубликовано' и дате."""
    filters = {
        'is_published': True,
        'pub_date__lte': timezone.now(),
        'category__is_published': True,
        **kwargs,
    }

    return queryset.filter(**filters).annotate(
        comment_count=Count('comments'))


def send_test_email(request):
    subject = 'Восстановление пароля'
    message = 'Направляем тестовое сообщение для восстановления пароля'
    from_email = 'test@example.com'
    recipient_list = ['recipient@example.com']

    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse('Test email sent.')
