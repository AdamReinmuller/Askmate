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


if __name__ == '__main__':
    new_content = {'id': 'vmi',
                   'submission_time': 'vmi',
                   'view_number': 'vmi',
                   'vote_number': 'valami',
                   'title': 'requ',
                   'message': 'request',
                   'image': 'valami'}
    print(util.get_headers('data/question.csv'))

