from page_analyzer.database import get_all_urls
import validators
from urllib.parse import urlparse


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
