import urllib
from datetime import datetime
import urllib.request
import os
import bcrypt


def get_time():
    dt = datetime.now().replace(second=0, microsecond=0)
    return dt


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
    value = bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
    return value
