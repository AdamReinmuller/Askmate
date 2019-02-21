import connection
import time
import util


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
