from psycopg2 import sql
import connection
import util

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
                            """,
                   {'table': table})
    keys_ = cursor.fetchall()
    headers = []
    for dict in keys_:
        headers.append(dict['column_name'])
    return headers


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
def delete_answer_by_id(cursor, id):
    cursor.execute('''
        SELECT question_id FROM answer
        WHERE id = %(id)s''', {'id': id})
    question_id = cursor.fetchone()
    cursor.execute('''
    DELETE FROM answer
    WHERE id = %(id)s''', {'id': id})
    return question_id


@connection.connection_handler
def delete_answer_by_question_id(cursor, question_id):
    cursor.execute('''
    DELETE FROM answer
    WHERE question_id = %(question_id)s''', {'question_id': question_id})


@connection.connection_handler
def delete_question(cursor, id_):
    cursor.execute('''
    DELETE FROM question_tag
    WHERE question_id=%(id_)s;
    DELETE FROM question
    WHERE id = %(id_)s;
    ''', {'id_': id_})


@connection.connection_handler
def get_question_by_id(cursor, id_):
    cursor.execute('''
    SELECT * FROM question
    WHERE id = %(id_)s''', {'id_': id_})
    question = cursor.fetchall()
    return question


@connection.connection_handler
def update_question(cursor, id_, title, message):
    cursor.execute("""UPDATE question
                      SET message = %(message)s,
                          title = %(title)s
                      WHERE id = %(id_)s
                        """,
                   dict(id_=id_, title=title, message=message)
                   )


@connection.connection_handler
def update_answer(cursor, id_, message):
    cursor.execute("""UPDATE answer
                      SET message = %(message)s
                      WHERE id = %(id_)s
                        """,
                   dict(id_=id_, message=message)
                   )


@connection.connection_handler
def change_vote_number_in_table(cursor, table, id_, method):
    """
    changes the vote number in question or answer db
    """
    if method == 'up':
        cursor.execute(sql.SQL("""
                            UPDATE {table}
                            SET vote_number = vote_number+1
                            WHERE id = %(id)s;
                           """).format(table=sql.Identifier(table)),
                       dict(id=id_)
                       )
    elif method == 'down':
        cursor.execute(sql.SQL("""
                                UPDATE {table}
                                SET vote_number = vote_number-1
                                WHERE id = %(id)s;
                               """).format(table=sql.Identifier(table)),
                       dict(id=id_)
                       )


@connection.connection_handler
def add_tag_to_question(cursor, question_id, tag):
    cursor.execute('''INSERT INTO tag (name) VALUES (%(tag)s)''', {'tag': tag})
    cursor.execute('''SELECT id FROM tag
    WHERE name = (%(tag)s)''', {'tag': tag})
    tag_id = cursor.fetchone()['id']
    cursor.execute('''
                      INSERT INTO question_tag
                      VALUES (%(question_id)s, %(tag_id)s)
                      '''
                   , {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def delete_tag(cursor, question_id, tag_id):
    cursor.execute('''DELETE FROM question_tag
                      WHERE question_id=%(question_id)s AND tag_id=%(tag_id)s;
                      DELETE FROM tag
                      WHERE id=%(tag_id)s;
                      ''',
                   {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def search(cursor, search_phrase):
    """
    :return: rows in the question_db and the correlated answer_db where the search_phrase is found
    """
    cursor.execute('''
                    SELECT DISTINCT question.*
                    FROM question
                    FULL JOIN answer
                    ON question.id = answer.question_id
                    WHERE question.message ILIKE %(search_phrase)s OR
                          question.title ILIKE %(search_phrase)s OR
                          answer.message ILIKE %(search_phrase)s
                ''', dict(search_phrase='%' + search_phrase + '%'))
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def search_answers(cursor, search_phrase):
    """
    :return: rows in answer db with the column:message, question_id
    """
    cursor.execute('''
        SELECT question_id, message FROM answer
        WHERE message ILIKE %(search_phrase)s
                    ''', dict(search_phrase='%' + search_phrase + '%'))
    answers = cursor.fetchall()
    return answers



#zsuzsi


@connection.connection_handler
def get_line_title_by_id(cursor, table, id):
    cursor.execute(sql.SQL("""
                    SELECT title FROM {table}
                    WHERE id = %(id)s
                   """).format(table=sql.Identifier(table)), {'id': id})
    title = cursor.fetchall()
    return title

@connection.connection_handler
def get_foreign_key_by_id(cursor, table, foreign_key_name, id):
    cursor.execute(sql.SQL("""
                    SELECT {foreign_key_name} FROM {table}
                    WHERE id = %(id)s
                   """).format(table=sql.Identifier(table), foreign_key_name=sql.Identifier(foreign_key_name)), {'id': id})
    title = cursor.fetchall()
    return title


@connection.connection_handler
def get_line_data_by_id(cursor, table, id):
    cursor.execute(sql.SQL("""
                    SELECT * FROM {table}
                    WHERE id = %(id)s
                    ORDER BY submission_time DESC;
                   """).format(table=sql.Identifier(table)), {'id': id})
    line_data = cursor.fetchall()
    return line_data


@connection.connection_handler
def get_comments_data_by_foreign_id(cursor, foreign_id_name, id):
    cursor.execute(sql.SQL("""
                    SELECT id, message, submission_time, edited_count FROM comment
                    WHERE {foreign_id_name} = %(id)s
                    ORDER BY submission_time DESC;
                   """).format(foreign_id_name=sql.Identifier(foreign_id_name)), {'id': id})
    comments_data = cursor.fetchall()
    return comments_data

@connection.connection_handler
def get_lines_data_by_foreign_id(cursor, table, foreign_id_name, id):
    cursor.execute(sql.SQL("""
                    SELECT * FROM {table}
                    WHERE {foreign_id_name} = %(id)s
                    ORDER BY submission_time DESC;
                   """).format(table=sql.Identifier(table), foreign_id_name=sql.Identifier(foreign_id_name)), {'id': id})
    lines_data = cursor.fetchall()
    return lines_data

@connection.connection_handler
def get_lines_data_by_not_foreign_id(cursor, table, foreign_id_name, id):
    cursor.execute(sql.SQL("""
                    SELECT * FROM {table}
                    WHERE {foreign_id_name} <> %(id)s
                    ORDER BY submission_time DESC;
                   """).format(table=sql.Identifier(table), foreign_id_name=sql.Identifier(foreign_id_name)), {'id': id})
    lines_data = cursor.fetchall()
    return lines_data


@connection.connection_handler
def add_comment_to_table(cursor, table, id_type, id, message, submission_time, edited_count):
    cursor.execute(sql.SQL("""
                    INSERT INTO {table} ({id_type}, message, submission_time, edited_count)
                    VALUES (%(id)s, %(message)s, %(submission_time)s, %(edited_count)s)
                   """).format(table=sql.Identifier(table), id_type=sql.Identifier(id_type)),
                   {'id': id, 'message': message, 'submission_time': submission_time, 'edited_count': edited_count})

@connection.connection_handler
def delete_line_by_id(cursor, table, id):
 cursor.execute(sql.SQL("""
                            DELETE FROM {table}
                            WHERE id = %(id)s;
                           """).format(table=sql.Identifier(table)),
                           {'id': id})

@connection.connection_handler
def delete_line_by_foreign_id(cursor, table, foreign_id_name, foreign_id):
 cursor.execute(sql.SQL("""
                            DELETE FROM {table}
                            WHERE {foreign_id_name} = %(foreign_id)s;
                           """).format(table=sql.Identifier(table), foreign_id_name=sql.Identifier(foreign_id_name)),
                           {'foreign_id': foreign_id})

@connection.connection_handler
def update_comment_message_submt_editedc_by_id(cursor, id, message, submission_time):
 cursor.execute(sql.SQL("""
                            UPDATE comment
                            SET edited_count = edited_count+1, message=%(message)s , submission_time=%(submission_time)s
                            WHERE id = %(id)s;
                           """).format(message=sql.Identifier(message), submission_time=sql.Identifier(str(submission_time))),
                           {'message': message, 'submission_time': submission_time, 'id': id})


@connection.connection_handler
def get_headers(cursor, table):
    cursor.execute(sql.SQL("""
                    SELECT * FROM {table};
                   """).format(table=sql.Identifier(table)))
    one_line_from_table_to_get_keys = cursor.fetchone()
    headers = util.get_headers(one_line_from_table_to_get_keys)
    return headers

@connection.connection_handler
def get_ids_by_foreign_id(cursor, table, foreign_id_name, foreign_id):
    cursor.execute(sql.SQL("""
                        SELECT id FROM {table}
                        WHERE {foreign_id_name} = %(foreign_id)s
                       """).format(table=sql.Identifier(table), foreign_id_name=sql.Identifier(foreign_id_name)),
                        {'foreign_id': foreign_id})
    ids = cursor.fetchall()
    return ids

@connection.connection_handler
def get_ids_by_not_foreing_id(cursor, table, foreign_id_name, foreign_id):
    cursor.execute(sql.SQL("""
                        SELECT id FROM {table}
                        WHERE {foreign_id_name} <> %(foreign_id)s
                       """).format(table=sql.Identifier(table), foreign_id_name=sql.Identifier(foreign_id_name)),
                        {'foreigh_id': foreign_id})
    ids = cursor.fetchall()
    return ids


@connection.connection_handler
def update_image_data_by_id(cursor, table, id, filename):
    cursor.execute(sql.SQL("""UPDATE {table}
                      SET image = %(filename)s
                      WHERE id = %(id)s
                        """).format(table=sql.Identifier(table)),
                   dict(id=id, filename=filename)
                   )