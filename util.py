import urllib
from datetime import datetime
import urllib.request
import connection
import os
import bcrypt


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

@connection.connection_handler
def get_questions_by_tag(cursor, tag_id):
    cursor.execute('''SELECT question_id FROM question_tag
                      WHERE tag_id=%(tag_id)s''', {'tag_id':tag_id})
    question_ids = [id['question_id'] for id in cursor.fetchall()]
    return question_ids

def save_image_to_file(url, filename):
    urllib.request.urlretrieve(url, filename)


def delete_file(filename):
    os.remove(filename)


def check_file(filename):
    return os.path.exists(filename)


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
