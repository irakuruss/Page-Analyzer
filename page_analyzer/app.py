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
from page_analyzer.validator import get_validation_errors, get_url_check, normalize_url
from page_analyzer.database import (
    add_url_to_db,
    get_url_by_id,
    get_all_urls,
    add_url_check_to_db,
    get_url_checks_by_id,
    get_last_url_check,
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
        last_check = get_last_url_check()
        return render_template('urls.html', urls=urls, last_check=last_check)
    url = request.form.to_dict()
    errors = get_validation_errors(url['url'])
    if errors:
        return render_template(
            'index.html',
            errors=errors
        ), 422
    url['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    url['url'] = normalize_url(url)
    is_added, id = add_url_to_db(url)
    if is_added:
        flash('Страница успешно добавлена', 'success')
    else:
        flash('Страница уже существует', 'info')
    return redirect(url_for('url_page', id=id))


@app.get('/urls/<int:id>')
def url_page(id):
    url = get_url_by_id(id)
    checks = get_url_checks_by_id(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html',
                           url=url,
                           messages=messages, checks=checks
                           )


@app.post('/urls/<int:id>/checks')
def add_check(id):
    url = get_url_by_id(id)
    try:
        check = get_url_check(id, url['name'])
        if check['status_code'] == 200:
            add_url_check_to_db(check)
            flash('Страница успешно проверена', 'success')
        else:
            flash('Произошла ошибка при проверке', 'error')
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'error')
    return redirect(url_for('url_page', id=id))
