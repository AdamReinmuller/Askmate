import connection
import time
import util
import urllib.request
import os


def save_image_to_file(url, filename):
    urllib.request.urlretrieve(url, filename)

def delete_file(filename):
    os.remove(filename)

def check_file(filename):
    return os.path.exists(filename)

def add_question(form_title, form_question):
    momentary_time = round(time.time())
    new_id = util.get_id('data/question.csv')
    nested_ordered_dict = connection.import_csv('data/question.csv')
    new_content = {'id': new_id,
                   'submission_time': momentary_time,
                   'view_number': 0,
                   'vote_number': 0,
                   'title': form_title,
                   'message': form_question,
                   'image': 'No image'
                   }
    nested_ordered_dict.append(new_content)
    connection.export_csv('data/question.csv', nested_ordered_dict)


def add_answer(question_id, form_answer):
    momentary_time = round(time.time())
    new_id = util.get_id('data/answer.csv')
    nested_ordered_dict = connection.import_csv('data/answer.csv')
    new_content = {'id': new_id,
                   'submission_time': momentary_time,
                   'vote_number': 0,
                   'question_id': question_id,
                   'message': form_answer,
                   'image': 'No image'
                   }
    nested_ordered_dict.append(new_content)
    connection.export_csv('data/answer.csv', nested_ordered_dict)


def get_ordered_dict_by_id(filename, id):
    """
    :param filename: relative path
    :param id: input id as integer
    :return: one ordered dict
    """
    nested_ordered_dicts = connection.import_csv(filename)
    for row in nested_ordered_dicts:
        if int(row['id']) == id:
            return row


def get_list_by_key(filename, data, key):
    """
    :param filename: relative path
    :param data: input data
    :param key: the key of the dictionary where i searh for the data
    :return: one ordered dict
    """
    result = []
    nested_ordered_dicts = connection.import_csv(filename)
    for row in nested_ordered_dicts:
        if int(row[key]) == data:
            result.append(row)
    return result

def get_list_by_not_key(filename, data, key):
    """
    :param filename: relative path
    :param data: input data
    :param key: the key of the dictionary where i searh for the data
    :return: one ordered dict
    """
    result = []
    nested_ordered_dicts = connection.import_csv(filename)
    for row in nested_ordered_dicts:
        if int(row[key]) != data:
            result.append(row)
    return result


def get_key_by_id(filename, key, id):
    nested_ordered_dicts = connection.import_csv(filename)
    for row in nested_ordered_dicts:
        if int(row['id']) == int(id):
            return row[key]


def delete_line_from_csv(filename, id_):
    nested_ordered_dicts = connection.import_csv(filename)
    remaining_rows = []
    for row in nested_ordered_dicts:
        if int(row['id']) == int(id_):
            pass
        else:
            remaining_rows.append(row)
    connection.export_csv(filename, remaining_rows)


def edit_line_from_csv(filename, id_, title, message):
    nested_ordered_dicts = connection.import_csv(filename)
    for row in nested_ordered_dicts:
        if int(row['id']) == id_:
            row['title'] = title
            row['message'] = message
            break
    connection.export_csv(filename, nested_ordered_dicts)


def update_line_from_csv(filename, id_, key, new_data):
    nested_ordered_dicts = connection.import_csv(filename)
    for row in nested_ordered_dicts:
        if int(row['id']) == id_:
            row[key] = new_data
    connection.export_csv(filename, nested_ordered_dicts)


def change_vote_number_in_csv(filename, id_, metod):
    nested_ordered_dicts = connection.import_csv(filename)
    for row in nested_ordered_dicts:
        if int(row['id']) == int(id_):
            if metod == 'up':
                row['vote_number'] = int(row['vote_number']) + 1
            else:
                row['vote_number'] = int(row['vote_number']) - 1

    connection.export_csv(filename, nested_ordered_dicts)
