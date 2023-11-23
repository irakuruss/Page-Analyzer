import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def add_url_to_db(url):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO urls (name, created_at) '
                           'VALUES (%s, %s);',
                           (url['url'], url['created_at']))
            conn.commit()
        except psycopg2.Error:
            conn.rollback()


def add_url_check_to_db(check):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO url_checks '
                       '(url_id, '
                       'status_code, '
                       'h1, '
                       'title, '
                       'description, '
                       'created_at) '
                       'VALUES (%s, %s, %s, %s, %s, %s);',
                       (check['url_id'],
                        check['status_code'],
                        check['h1'],
                        check['title'],
                        check['description'],
                        check['created_at']))
        conn.commit()


def get_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM urls '
                       'WHERE id = (%s);',
                       [id])
        url = cursor.fetchone()
    return url


def get_url_by_name(name):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        try:
            cursor.execute('SELECT id FROM urls '
                           'WHERE name = (%s)',
                           [name])
            return cursor.fetchone()[0]
        except Exception:
            return


def get_all_urls():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT MAX(url_checks.created_at) AS created_at, '
                       'urls.id, urls.name, url_checks.status_code '
                       'FROM urls LEFT JOIN url_checks '
                       'ON urls.id = url_checks.url_id '
                       'GROUP BY urls.id, url_checks.status_code '
                       'ORDER BY urls.id DESC;')
        all_urls = cursor.fetchall()
    return all_urls


def get_url_checks_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM url_checks '
                       'WHERE url_id = (%s)'
                       'ORDER BY id DESC;',
                       [id])
        url_checks = cursor.fetchall()
    return url_checks
