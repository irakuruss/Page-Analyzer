from page_analyzer.database import get_all_urls
import validators
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def validate(url):  # noqa: C901
    errors = {}
    all_orders = get_all_urls()
    existed_sites = []
    for order in all_orders:
        existed_sites.append(order[1])
    parsed_name = urlparse(url['url'])
    normalize_name = '{0}://{1}'.format(
        parsed_name.scheme,
        parsed_name.netloc
    )
    if normalize_name != '://':
        url['url'] = normalize_name
    for elem in existed_sites:
        if elem.startswith(url['url']):
            errors['name'] = 'Страница уже существует'
    if not validators.url(url['url']):
        errors['name'] = 'Некорректный URL'
        if not url['url']:
            errors['name1'] = 'URL обязателен'
    return errors


def get_check_url(id, url):
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
