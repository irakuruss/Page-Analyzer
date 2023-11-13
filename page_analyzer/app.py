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
from page_analyzer.validator import validate
from page_analyzer.database import (
    add_url_to_db,
    get_url_by_name,
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


@app.post('/urls')
def add_url():
    url_fields_dct = request.form.to_dict()
    url_fields_dct['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    errors = validate(url_fields_dct)
    if errors:
        if errors['name'] == 'Страница уже существует':
            url_tuple = get_url_by_name(url_fields_dct['url'])
            id = url_tuple[0]
            flash(errors['name'], 'alert-primary')
            return redirect(url_for('get_one_url', id=id))
        flash(errors['name'], 'alert-danger')
        if 'name1' in errors.keys():
            flash(errors['name1'], 'alert-danger')
        errors = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            url_fields_dct=url_fields_dct,
            errors=errors
        )
    else:
        add_url_to_db(url_fields_dct)
        flash('Адрес добавлен', 'alert-success')
        id = get_url_by_name(url_fields_dct['url'])[0]
        return redirect(url_for('get_one_url', id=id))


@app.get('/urls')
def get_urls():
    all_urls = get_all_urls()
    checks = get_last_url_check()
    return render_template('urls.html', urls=all_urls, checks=checks)


@app.get('/urls/<id>')
def get_one_url(id):
    url = get_url_by_id(id)
    checks = get_url_checks_by_id(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html',
                           url=url,
                           messages=messages, checks=checks
                           )


@app.post('/urls/<id>/checks')
def add_check(id):
    url = get_url_by_id(id)[1]
    try:
        r = requests.get(url, verify=False)
        code = r.status_code
        check = {'url_id': id,
                        'status_code': code,
                        'created_at': datetime.now().strftime('%Y-%m-%d')
                        }
        add_url_check_to_db(check)
    except requests.ConnectionError:
        flash('Произошла ошибка при проверке', 'alert-danger')
    return redirect(url_for('get_one_url', id=id))
