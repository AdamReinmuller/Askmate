from datetime import datetime
import urllib.request
import connection
import os

@connection.connection_handler
def get_last_question_id(cursor):
    cursor.execute('''SELECT id FROM question ORDER BY ID DESC LIMIT 1''')
    last_question_id = cursor.fetchone()
    return last_question_id['id']


def get_time():
    dt = datetime.now().replace(second=0, microsecond=0)
    return dt


@connection.connection_handler
def get_tag(cursor, id_=1):
    try:
        cursor.execute('''  SELECT tag_id FROM question_tag
                            WHERE question_id = %(id_)s''', {'id_': id_})
        tag_id = cursor.fetchone()['tag_id']
        cursor.execute('''  SELECT name FROM tag
                            WHERE id = %(tag_id)s''', {'tag_id': tag_id})
        tags_dict = cursor.fetchall()
        tag = tags_dict[0]['name']
        return tag
    except TypeError:
        return False


def get_headers(table_):
    headers = table_.keys()
    return headers


def save_image_to_file(url, filename):
    urllib.request.urlretrieve(url, filename)


def delete_file(filename):
    os.remove(filename)


def check_file(filename):
    return os.path.exists(filename)
