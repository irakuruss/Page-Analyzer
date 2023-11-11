import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def add_url_to_db(data):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                       (data['url'], data['created_at']))
    conn.commit()
    conn.close()


def get_url_by_name(name):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM urls WHERE name = (%s)', [name])
        url_tuple = cursor.fetchone()
    conn.close()
    return url_tuple


def get_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM urls WHERE id = (%s)', [id])
        url_tuple = cursor.fetchone()
    conn.close()
    return url_tuple


def get_all_urls():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM urls')
        all_urls = cursor.fetchall()
    conn.close()
    return all_urls
