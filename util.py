import urllib
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
def get_tags(cursor, id_=None):
    try:
        cursor.execute('''  SELECT tag_id FROM question_tag
                            WHERE question_id = %(id_)s''', {'id_': id_})
        tags_id = tuple(id['tag_id'] for id in cursor.fetchall())
        cursor.execute('''  SELECT name, id FROM tag
                            WHERE id IN %(tags_id)s''', {'tags_id': tags_id})
        tags_dict = cursor.fetchall()
        return tags_dict
    except:
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
