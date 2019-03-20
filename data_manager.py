from psycopg2 import sql
import connection
import util

question_db = 'question'
answer_db = 'answer'
comment_db = 'comment'
tag_db = 'tag'
question_tag_db = 'question_tag'
users_db = 'users'


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
def add_question(cursor, title, message, users_id):
    """
    :return: writes to question_db
    """
    current_time = util.get_time()
    cursor.execute("""INSERT INTO question
                      (submission_time, view_number, vote_number, title, message, image, users_id)
                      VALUES ( %(submission_time)s, 0, 0, %(title)s, %(message)s, 'no image', %(users_id)s )
                    """,
                   dict(submission_time=current_time, title=title, message=message, users_id=users_id)
                   )


@connection.connection_handler
def add_answer(cursor, question_id, message, users_id):
    """
    :return: writes to answer_db
    """
    current_time = util.get_time()
    cursor.execute("""INSERT INTO answer
                      (submission_time, vote_number, question_id, message, image, users_id, accepted_status)
                      VALUES ( %(submission_time)s, 0, %(question_id)s, %(message)s, 'no image', %(users_id)s, FALSE)
                    """,
                   dict(submission_time=current_time, question_id=question_id, message=message, users_id=users_id)
                   )


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
def accept_answer(cursor, id_):
    cursor.execute("""UPDATE answer
                      SET accepted_status = TRUE
                      WHERE id = %(id_)s
                        """,
                   dict(id_=id_)
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
    cursor.execute('''SELECT * FROM tag
                    WHERE name = %(tag)s''', {'tag': tag})
    on_the_table = cursor.fetchall()
    if not on_the_table:
        cursor.execute('''INSERT INTO tag (name) VALUES (%(tag)s);
                          SELECT id FROM tag
                          WHERE name = (%(tag)s)''', {'tag': tag})
        tag_id = cursor.fetchone()['id']
        cursor.execute('''
                          INSERT INTO question_tag
                          VALUES (%(question_id)s, %(tag_id)s)
                          '''
                       , {'question_id': question_id, 'tag_id': tag_id})
    elif on_the_table:
        cursor.execute('''SELECT id FROM tag
        WHERE name = %(tag)s''', {'tag': tag})
        tag_id = cursor.fetchone()['id']
        cursor.execute('''SELECT * FROM question_tag
                          WHERE tag_id=%(tag_id)s AND question_id=%(question_id)s''',
                       {'question_id': question_id, 'tag_id': tag_id})
        existing_question_tag_connection = cursor.fetchall()
        if not existing_question_tag_connection:
            cursor.execute('''INSERT INTO question_tag
                              VALUES (%(question_id)s, %(tag_id)s)''',
                           {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def delete_tag(cursor, question_id, tag_id):
    cursor.execute('''DELETE FROM question_tag
                      WHERE question_id=%(question_id)s AND tag_id=%(tag_id)s;
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
                    SELECT id, message, submission_time, edited_count, users_id FROM comment
                    WHERE {foreign_id_name} = %(id)s
                    ORDER BY submission_time DESC;
                   """).format(foreign_id_name=sql.Identifier(foreign_id_name)), {'id': id})
    comments_data = cursor.fetchall()
    return comments_data


@connection.connection_handler
def get_question_comments_message_with_question_by_foreign_id(cursor, foreign_id_name, id):
    cursor.execute(sql.SQL("""
                    SELECT comment.message, comment.question_id, title FROM comment join question on question_id=question.id
                    WHERE question_id is not null And comment.{foreign_id_name} = %(id)s 
                    ORDER BY comment.message ASC;
                   """).format(foreign_id_name=sql.Identifier(foreign_id_name)), {'id': id})
    comments_data = cursor.fetchall()
    return comments_data

@connection.connection_handler
def get_answer_comments_message_with_answer_and_question_by_foreign_id(cursor, foreign_id_name, id):
    cursor.execute(sql.SQL("""
                    SELECT comment.message AS "comment message", comment.answer_id, answer.message AS "answer message", answer.question_id, title 
                    FROM (comment join answer on answer_id=answer.id) join question on answer.question_id=question.id
                    WHERE answer_id is not null And comment.{foreign_id_name} = %(id)s 
                    ORDER BY comment.message ASC;
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
def get_answers_with_their_questions_by_foreign_id(cursor, foreign_id_name, id):
    cursor.execute(sql.SQL("""
                    SELECT answer.message, question.id AS question_id, question.title FROM answer join question on question_id=question.id
                    WHERE answer.{foreign_id_name} = %(id)s
                    ORDER BY answer.message ASC;
                   """).format(foreign_id_name=sql.Identifier(foreign_id_name)), {'id': id})
    lines_data = cursor.fetchall()
    return lines_data



@connection.connection_handler
def add_comment_to_table(cursor, table, id_type, id, message, submission_time, edited_count, users_id):
    cursor.execute(sql.SQL("""
                    INSERT INTO {table} ({id_type}, message, submission_time, edited_count, users_id)
                    VALUES (%(id)s, %(message)s, %(submission_time)s, %(edited_count)s, %(users_id)s)
                   """).format(table=sql.Identifier(table), id_type=sql.Identifier(id_type)),
                   {'id': id, 'message': message, 'submission_time': submission_time, 'edited_count': edited_count, 'users_id': users_id})


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
                           """).format(message=sql.Identifier(message),
                                       submission_time=sql.Identifier(str(submission_time))),
                   {'message': message, 'submission_time': submission_time, 'id': id})


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
def update_image_data_by_id(cursor, table, id, new_data):
    cursor.execute(sql.SQL("""UPDATE {table}
                      SET image = %(new_data)s
                      WHERE id = %(id)s
                        """).format(table=sql.Identifier(table)),
                   dict(id=id, new_data=new_data)
                   )


@connection.connection_handler
def update_view_number_in_question_by_id(cursor, id):
    cursor.execute("""UPDATE question
                      SET view_number = view_number+1
                      WHERE id = %(id)s
                        """, {'id': id})


@connection.connection_handler
def get_five_latest_submitted_titles_with_ids_from_table(cursor, table):
    cursor.execute(sql.SQL("""
                    SELECT title, id FROM {table} 
                    ORDER BY submission_time DESC
                    LIMIT 5
                   """).format(table=sql.Identifier(table)))
    five_latest_titles_with_ids_from_table = cursor.fetchall()
    return five_latest_titles_with_ids_from_table

@connection.connection_handler
def get_tags_and_question_count(cursor):
    cursor.execute('''SELECT tag.id, tag.name, COUNT(question_id) FROM tag JOIN question_tag
                        ON tag.id = question_tag.tag_id
                        GROUP BY tag.id
                        ORDER BY tag.id''')
    data = cursor.fetchall()
    return data

@connection.connection_handler
def get_questions_by_tag(cursor, tag_name):
    cursor.execute('''SELECT question.*
                      FROM tag JOIN question_tag ON tag.id = question_tag.tag_id
                      JOIN question ON question_tag.question_id = question.id
                      WHERE tag.name = %(tag_name)s''', {'tag_name':tag_name})
    data = cursor.fetchall()
    return data

if __name__ == '__main__':
    print(get_tags_and_question_count())


@connection.connection_handler
def get_last_question_id(cursor):
    cursor.execute('''SELECT id FROM question ORDER BY ID DESC LIMIT 1''')
    last_question_id = cursor.fetchone()
    return last_question_id['id']


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
def get_tags_and_question_count(cursor):
    cursor.execute('''SELECT tag.id, tag.name, COUNT(question_id) FROM tag JOIN question_tag
                        ON tag.id = question_tag.tag_id
                        GROUP BY tag.id
                        ORDER BY tag.id''')
    data = cursor.fetchall()
    return data

@connection.connection_handler
def get_questions_by_tag(cursor, tag_name):
    cursor.execute('''SELECT question.*
                      FROM tag JOIN question_tag ON tag.id = question_tag.tag_id
                      JOIN question ON question_tag.question_id = question.id
                      WHERE tag.name = %(tag_name)s''', {'tag_name':tag_name})
    data = cursor.fetchall()
    return data


@connection.connection_handler
def register_user(cursor, username, plain_text_password):
    password = util.hash_password(plain_text_password)
    current_date = util.get_time()
    cursor.execute(("""
                    INSERT INTO users
                    (username, password, reputation, registration_date)
                    VALUES (%(username)s, %(password)s, 0, %(registration_date)s)
                   """), dict(username=username, password=password, registration_date=current_date))


@connection.connection_handler
def get_userid_by_username(cursor, username):
    cursor.execute("""
                        SELECT id FROM users
                        WHERE username = %(username)s
                       """, {'username': username})
    try:
        id = cursor.fetchone()['id']
        return id
    except:
        return False

@connection.connection_handler
def get_hashpw_of_username(cursor, username):
    cursor.execute("""
                        SELECT password FROM users
                        WHERE username = %(username)s
                       """, {'username': username})
    try:
        hashpw = cursor.fetchone()['password']
        return hashpw
    except:
        return False
