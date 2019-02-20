import connection
import time
from flask import request
import util

def new_question(form_title, form_question):
    momentary_time = round(time.time())
    new_id = util.get_id('data/question.csv')
    new_content = {'id': new_id,
                   'submission_time': momentary_time,
                   'view_number': 0,
                   'vote_number': 0,
                   'title': form_title,
                   'message': form_question,
                   'image': 'No image'
                   }
    connection.export_csv('data/question.csv', new_content)

def delete_answer_from_csv(id_):
    table = connection.import_csv('data/answer.csv')
    temp = []
    for answer in table:
        if answer['id'] == id_:
            pass
        else:
            temp.append(answer)
    connection.export_csv('data/answer.csv', temp)


def delete_question_from_csv(id_):
    table = connection.import_csv('data/question.csv')
    temp = []
    for answer in table:
        if answer['id'] == id_:
            pass
        else:
            temp.append(answer)
    connection.export_csv('data/question.csv', temp)



if __name__ == '__main__':
    delete_question_from_csv('1')