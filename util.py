from datetime import datetime
import connection
import urllib.request
import os

@connection.connection_handler
def get_last_question_id(cursor):
    cursor.execute('''
    SELECT id FROM question ORDER BY ID DESC LIMIT 1''')
    last_question_id = cursor.fetchone()
    return last_question_id['id']


def get_time():
    dt = datetime.now().replace(second=0, microsecond=0)
    return dt


def get_headers(table_):
    headers = table_.keys()
    return headers


def save_image_to_file(url, filename):
    urllib.request.urlretrieve(url, filename)


def delete_file(filename):
    os.remove(filename)


def check_file(filename):
    return os.path.exists(filename)
