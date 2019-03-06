from datetime import datetime
import connection

@connection.connection_handler
def get_last_question_id(cursor):
    cursor.execute('''
    SELECT id FROM question ORDER BY ID DESC LIMIT 1''')
    last_question_id = cursor.fetchall()
    return last_question_id


def get_time():
    dt = datetime.now()
    return dt
