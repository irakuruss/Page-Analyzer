import validators
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import flash, get_flashed_messages


MAX_LENGTH = 255


def normalize_url(url):
    parse_url = urlparse(url)
    return f'{parse_url.scheme}://{parse_url.netloc}'


def get_valid_length(data):
    if data:
        if len(data) > MAX_LENGTH:
            data = data[:MAX_LENGTH-3] + '...'
    return data


def get_validation_errors(url):
    if not validators.url(url):
        if not url:
            flash('URL обязателен', 'danger')
        else:
            flash('Некорректный URL', 'danger')
    if len(url) > MAX_LENGTH:
        flash(f'URL превышает {MAX_LENGTH} символов', 'danger')
    return get_flashed_messages(with_categories=True)


def get_parse_data(data):
    soup = BeautifulSoup(data.text, 'html.parser')
    h1, title, description = '', '', ''
    if soup.h1:
        h1 = soup.h1.string
    if soup.title:
        title = soup.title.string
    if soup.find(attrs={'name': 'description'}):
        description = soup.find(attrs={'name': 'description'})['content']
    return h1, title, description


def get_url_check(id, url):
    parse_data = requests.get(url)
    h1, title, description = get_parse_data(parse_data)
    check = {'url_id': id,
             'status_code': parse_data.status_code,
             'h1': get_valid_length(h1),
             'title': get_valid_length(title),
             'description': get_valid_length(description),
             'created_at': datetime.now().strftime('%Y-%m-%d')
             }
    return check
