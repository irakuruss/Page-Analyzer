from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    flash,
    get_flashed_messages,
)
import os
from datetime import datetime
from dotenv import load_dotenv
import requests
from page_analyzer.validator import (
    get_validation_errors,
    normalize_url)
from page_analyzer.url_check import get_url_check
from page_analyzer.database import (
    add_url_to_db,
    get_url_by_id,
    get_all_urls,
    add_url_check_to_db,
    get_url_checks_by_id,
    get_url_by_name,
    get_last_checks
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls_page():
    if request.method == 'GET':
        urls = get_all_urls()
        last_check = get_last_checks()
        return render_template('urls.html', urls=urls, last_check=last_check)
    url = request.form.to_dict()
    errors = get_validation_errors(url['url'])
    if errors:
        return render_template(
            'index.html',
            errors=errors
        ), 422
    url['url'] = normalize_url(url['url'])
    id = get_url_by_name(url['url'])
    if id:
        flash('Страница уже существует', 'info')
        return redirect(url_for('url_page', id=id))
    url['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_url_to_db(url)
    id = get_url_by_name(url['url'])
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_page', id=id))


@app.get('/urls/<int:id>')
def url_page(id):
    url = get_url_by_id(id)
    checks = get_url_checks_by_id(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html',
                           url=url,
                           messages=messages,
                           checks=checks
                           )


@app.post('/urls/<int:id>/checks')
def add_check(id):
    url = get_url_by_id(id)
    try:
        requests.get(url['name']).raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        check = get_url_check(id, url['name'])
        add_url_check_to_db(check)
        flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_page', id=id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_server_error.html'), 500
