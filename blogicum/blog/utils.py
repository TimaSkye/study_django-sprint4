from .constants import TRUNCATE_LENGTH


def truncate_text(text, truncate_length=TRUNCATE_LENGTH):
    """Функция обрезки строк."""
    if not text:
        return ''
    return (text[:truncate_length] + (
        '...' if len(text) > truncate_length else ''))
