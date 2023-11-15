# from page_analyzer.database import get_all_urls
import validators
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import flash, get_flashed_messages


def normalize_url(url):
    parse_url = urlparse(url)
    return f'{parse_url.scheme}://{parse_url.netloc}'


def get_valid_length(data):
    if data:
        if len(data) > 255:
            data = data[:252] + '...'
    return data


def get_valid_url(url):
    return validators.url(url) is True


def get_validation_errors(url):
    if not validators.url(url):
        flash('Некорректный URL', 'danger')
        if not url:
            flash('URL обязателен', 'danger')
    if len(url) > 255:
        flash('URL превышает 255 символов', 'danger')
    return get_flashed_messages(with_categories=True)


def get_url_check(id, url):
    r = requests.get(url)
    code = r.status_code
    html_file = r.text
    soup = BeautifulSoup(html_file, 'html.parser')
    if soup.h1:
        h1 = soup.h1.string
    else:
        h1 = ''
    if soup.title:
        title = soup.title.string
    else:
        title = ''
    if soup.find(attrs={'name': 'description'}):
        find_description = soup.find(attrs={'name': 'description'})
        description = find_description['content']
    else:
        description = ''
    check_record = {'url_id': id,
                    'status_code': code,
                    'h1': h1,
                    'title': title,
                    'description': description,
                    'created_at': datetime.now().strftime('%Y-%m-%d')
                    }
    return check_record
