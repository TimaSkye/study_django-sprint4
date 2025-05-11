from django.db.models import Count
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
