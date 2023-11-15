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
            cursor.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                           (url['url'], url['created_at']))
            conn.commit()
            is_added = True
        except psycopg2.Error:
            conn.rollback()
            is_added = False
        cursor.execute('SELECT id FROM urls WHERE name = (%s)',
                       [url['url']])
        id = cursor.fetchone()[0]
        return is_added, id


def get_url_by_name(name):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM urls WHERE name = (%s)', [name])
        url = cursor.fetchone()
    return url


def get_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM urls WHERE id = (%s)', [id])
        url = cursor.fetchone()
    return url


def get_all_urls():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM urls')
        all_urls = cursor.fetchall()
    return all_urls


def add_url_check_to_db(check):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO url_checks'
                       '(url_id,'
                       'status_code,'
                       'h1,'
                       'title,'
                       'description,'
                       'created_at)'
                       'VALUES (%s, %s, %s, %s, %s, %s)',
                       (check['url_id'],
                        check['status_code'],
                        check['h1'],
                        check['title'],
                        check['description'],
                        check['created_at']))
        conn.commit()


def get_url_checks_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM url_checks WHERE url_id = (%s)', [id])
        url_checks = cursor.fetchall()
    return url_checks


def get_last_url_check():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT'
                       'urls.id,'
                       'urls.name,'
                       'url_checks.status_code,'
                       'url_checks.created_at'
                       'FROM urls'
                       'LEFT JOIN url_checks ON urls.id = url_id'
                       'AND url_checks.id = (SELECT MAX(url_checks.id)'
                       'FROM url_checks'
                       'WHERE url_id = urls.id)'
                       'ORDER BY url_checks.created_at DESC')
        url_check = cursor.fetchall()
    return url_check
