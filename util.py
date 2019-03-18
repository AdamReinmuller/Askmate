import urllib
from datetime import datetime
import urllib.request
import os


def get_time():
    dt = datetime.now().replace(second=0, microsecond=0)
    return dt


def save_image_to_file(url, filename):
    urllib.request.urlretrieve(url, filename)


def delete_file(filename):
    os.remove(filename)


def check_file(filename):
    return os.path.exists(filename)
