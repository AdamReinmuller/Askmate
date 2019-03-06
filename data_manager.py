import collections
from psycopg2 import sql
import connection
import util
import urllib.request
import os


question_db = 'question'
answer_db = 'answer'
comment_db = 'comment'
tag_db = 'tag'
question_tag_db = 'question_tag'


@connection.connection_handler
def get_column_names_of_table(cursor, table):
    cursor.execute("""
                                SELECT column_name
                                FROM information_schema.columns
                                WHERE table_name   = %(table)s
                                AND is_nullable = 'YES'
                            """,
                              {'table': table})
    keys_ = cursor.fetchall()
    return keys_


@connection.connection_handler
def import_from_db(cursor, table):
    """
    :return: list of ordered dicts
    """
    cursor.execute(
        sql.SQL("SELECT * FROM {table} ").
            format(table=sql.Identifier(table))
    )
    names = cursor.fetchall()
    return names


def sort_table(table, key="", sort=""):
    """
    :key: by what fieldname you sort it
    :sort: asc or desc
    :return: questions in a list of ordered dictionaries
    """
    questions = import_from_db(table)
    if sort == 'desc':
        try:
            questions = sorted(questions, key=lambda x: int(x[key]), reverse=True)
        except:
            questions = sorted(questions, key=lambda x: x[key], reverse=True)
    elif sort == 'asc':
        try:
            questions = sorted(questions, key=lambda x: int(x[key]), reverse=False)
        except:
            questions = sorted(questions, key=lambda x: x[key], reverse=False)
    return questions


def save_image_to_file(url, filename):
    urllib.request.urlretrieve(url, filename)


def delete_file(filename):
    os.remove(filename)


def check_file(filename):
    return os.path.exists(filename)


@connection.connection_handler
def add_question(cursor, title, message):
    """
    :return: writes to question_db
    """
    current_time = util.get_time()
    cursor.execute("""INSERT INTO question
                      (submission_time, view_number, vote_number, title, message, image)
                      VALUES ( %(submission_time)s, 0, 0, %(title)s, %(message)s, 'no image' )
                    """,
                   dict(submission_time=current_time, title=title, message=message)
                   )


@connection.connection_handler
def add_answer(cursor, question_id, message):
    """
    :return: writes to answer_db
    """
    current_time = util.get_time()
    cursor.execute("""INSERT INTO answer
                      (submission_time, vote_number, question_id, message, image)
                      VALUES ( %(submission_time)s, 0, %(question_id)s, %(message)s, 'no image' )
                    """,
                   dict(submission_time=current_time, question_id=question_id, message=message)
                   )


def get_ordered_dict_by_id(table, id):
    """
    :param table: database's table
    :param id: input id as integer
    :return: one ordered dict
    """
    nested_ordered_dicts = import_from_db(table)
    for row in nested_ordered_dicts:
        if int(row['id']) == id:
            return row


def get_list_by_key(table, data, key):
    """
    :param table: database's table
    :param data: input data
    :param key: the key of the dictionary where i searh for the data
    :return: one ordered dict
    """
    result = []
    nested_ordered_dicts = import_from_db(table)
    for row in nested_ordered_dicts:
        if int(row[key]) == data:
            result.append(row)
    return result


def get_list_by_not_key(table, data, key):
    """
    :param table: database's table
    :param data: input data
    :param key: the key of the dictionary where i searh for the data
    :return: one ordered dict
    """
    result = []
    nested_ordered_dicts = import_from_db(table)
    for row in nested_ordered_dicts:
        if int(row[key]) != data:
            result.append(row)
    return result


def get_key_by_id(table, key, id):
    nested_ordered_dicts = import_from_db(table)
    for row in nested_ordered_dicts:
        if int(row['id']) == int(id):
            return row[key]

@connection.connection_handler
def delete_answer(cursor, id_):
    cursor.execute('''
        SELECT id FROM question
        WHERE id = %(id_)s''', {'id_': id_})
    question_id = cursor.fetchall()
    cursor.execute('''
    DELETE FROM answer
    WHERE id = %(id_)s''', {'id_':id_})
    return question_id

@connection.connection_handler
def delete_question(cursor, id_):
    cursor.execute('''
    DELETE FROM question
    WHERE id = %(id_)s''', {'id_':id_})


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
