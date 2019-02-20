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
    nested_ordered_dict.insert(0, new_content)
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
    nested_ordered_dict.insert(0, new_content)
    connection.export_csv('data/answer.csv', new_content)


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


def get_list_by_key(filename, id, key):
    """
    :param filename: relative path
    :param id: input id as integer
    :param key: the key of the dictionary where i searh for the id
    :return: one ordered dict
    """
    result = []
    nested_ordered_dicts = connection.import_csv(filename)
    for row in nested_ordered_dicts:
        if int(row[key]) == id:
            result.append(row)
    return result


def delete_line_from_csv(filename, id_):
    table = connection.import_csv(filename)
    temp = []
    for answer in table:
        if answer['id'] == id_:
            pass
        else:
            temp.append(answer)
    connection.export_csv(filename, temp)
