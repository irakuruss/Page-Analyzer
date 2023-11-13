import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def add_url_to_db(url):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                       (url['url'], url['created_at']))
    conn.commit()
    conn.close()


def get_url_by_name(name):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM urls WHERE name = (%s)', [name])
        url = cursor.fetchone()
    conn.close()
    return url


def get_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM urls WHERE id = (%s)', [id])
        url = cursor.fetchone()
    conn.close()
    return url


def get_all_urls():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM urls')
        all_urls = cursor.fetchall()
    conn.close()
    return all_urls


def add_url_check_to_db(check):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO url_checks (url_id, created_at)'
                       'VALUES (%s, %s)',
                       (check['url_id'], check['created_at']))
    conn.commit()
    conn.close()


def get_url_checks_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM url_checks WHERE url_id = (%s)', [id])
        url_checks = cursor.fetchall()
    conn.close()
    return url_checks


def get_last_url_check(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('SELECT MAX(created_at) FROM url_checks'
                       'WHERE url_id = (%s)', [id])
        url_check = cursor.fetchone()
    conn.close()
    return url_check
