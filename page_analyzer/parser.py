from bs4 import BeautifulSoup


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
