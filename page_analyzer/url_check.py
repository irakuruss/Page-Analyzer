import requests
from page_analyzer.parser import get_parse_data
from page_analyzer.validator import get_valid_length
from datetime import datetime


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
