import validators
from urllib.parse import urlparse
from flask import flash, get_flashed_messages


MAX_LENGTH = 255


def normalize_url(url):
    parse_url = urlparse(url)
    return f'{parse_url.scheme}://{parse_url.netloc}'


def get_valid_length(data):
    if data:
        if len(data) > MAX_LENGTH:
            data = data[:MAX_LENGTH - 3] + '...'
    return data


def get_validation_errors(url):
    if not validators.url(url):
        if not url:
            flash('URL обязателен', 'danger')
        else:
            flash('Некорректный URL', 'danger')
    elif len(url) > MAX_LENGTH:
        flash(f'URL превышает {MAX_LENGTH} символов', 'danger')
    return get_flashed_messages(with_categories=True)
