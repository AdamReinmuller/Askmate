from datetime import datetime


def get_headers(file):
    file_all = connection.import_csv(file)
    headers = list(file_all[0].keys())
    return headers


def get_date():
    dt = datetime.now()
    return dt

