import os
import psycopg2
import psycopg2.extras
from psycopg2 import sql


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper


@connection_handler
def insert_row(cursor, table, dict):
    """
    insert dict to database's table, order sensitive
    :param table: database table name
    :param dict: data to add
    """
    row_to_insert = get_column_names_of_table(table)
    for key in dict:
        row_to_insert[key] = dict[key]
    insert_values = list(row_to_insert.values())
    asd = sql.SQL(",").join(map(sql.Identifier, insert_values))

    cursor.execute(
        sql.SQL("INSERT INTO {table} VALUES {data};").
            format(data=asd,
                   table=sql.Identifier(table))
    )