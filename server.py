import collections

from flask import Flask, render_template, request, redirect
import data_manager

app = Flask(__name__)


@app.route('/')
def index():
    questions = data_manager.get_table(data_manager.question_db)
    if request.args:
        questions = data_manager.get_table(data_manager.question_db, request.args['order_by'], request.args['order_direction'])
    return render_template('list.html', questions=questions)


@app.route('/add-question', methods=['GET', 'POST'])
def post_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    elif request.method == 'POST':
        data = collections.OrderedDict(request.form)
        data_manager.add_question(data)
        return redirect('/')


@app.route('/question/<question_id>', methods=['GET', 'POST'])
@app.route('/question/<question_id>/add-answer', methods=['GET', 'POST'])
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.path == '/question/' + question_id + '/add-answer' and request.method == 'POST':
        message = request.form['message']
        data_manager.write_to_answers(question_id, message)
        return redirect('/question/' + question_id)
    elif request.path == '/question/' + question_id + '/add-answer' and request.method == 'GET':
        return render_template('add-answer.html', question=question)
    elif request.method == 'GET':
        answers = data_manager.get_answers(question_id)
        if len(answers) > 0:
            return render_template('question.html', question=question, answers=answers)
        else:
            return render_template('question.html', question=question)


@app.route('/answer/<answer_id>/delete')
@app.route('/question/<question_id>/delete')
def delete_qa(question_id="", answer_id=""):
    if request.path == '/question/' + question_id + '/delete':
        data_manager.delete_question_by_id(question_id)
        return redirect('/')
    elif request.path == '/answer/' + answer_id + '/delete':
        question_id = data_manager.get_question_id_of_answer(answer_id)
        data_manager.delete_answer_by_id(answer_id)
        return redirect('/question/' + question_id)


@app.route('/edit-question/<question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        data_manager.edit_question(question_id, title, message)
        return redirect('/question/' + question_id)
    elif request.method == 'GET':
        question = data_manager.get_question_by_id(question_id)
        return render_template('edit-question.html', question=question)


@app.route('/edit-answer/<answer_id>', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'POST':
        question_id = data_manager.get_question_id_of_answer(answer_id)
        message = request.form['message']
        data_manager.edit_answer(answer_id, message)
        return redirect('/question/' + question_id)
    elif request.method == 'GET':
        answer = data_manager.get_answer_by_id(answer_id)
        return render_template('edit-answer.html', answer=answer)


if __name__ == '__main__':
    app.run(debug=True, port=8000)


# from flask import Flask, request, render_template, redirect
# import util
# import connection
# import data_manager
#
# app = Flask(__name__)
#
# @app.route('/')
# @app.route('/list')
# def route_list():
#     questions = sorted(connection.import_csv('data/question.csv'), key=lambda k: int(k['id']), reverse=True)
#     headers = util.get_headers('data/question.csv')
#
#     return render_template('list.html', questions=questions, headers=headers)
#
#
# @app.route('/list/')
# def route_sorted_list():
#     try:
#         if request.args['order_direction'] == 'desc':
#             questions = sorted(connection.import_csv('data/question.csv'), key=lambda k: int(k[request.args['order_by']]), reverse=True)
#         else:
#             questions = sorted(connection.import_csv('data/question.csv'), key=lambda k: int(k[request.args['order_by']]), reverse=False)
#     except:
#         if request.args['order_direction'] == 'desc':
#             questions = sorted(connection.import_csv('data/question.csv'), key=lambda k: k[request.args['order_by']], reverse=True)
#         else:
#             questions = sorted(connection.import_csv('data/question.csv'), key=lambda k: k[request.args['order_by']], reverse=False)
#     headers = util.get_headers('data/question.csv')
#
#     return render_template('list.html', questions=questions, headers=headers)
#
#
# @app.route('/question/<int:question_id>')
# def route_question(question_id):
#     question = data_manager.get_ordered_dict_by_id('data/question.csv', question_id)
#     headers_q = util.get_headers('data/question.csv')
#     answers = data_manager.get_list_by_key('data/answer.csv', question_id, 'question_id')
#     headers_a = util.get_headers('data/answer.csv')
#     filename_q = '/static/image_for_question' + str(question_id) + '.png'
#     image_q = data_manager.check_file(filename_q.lstrip("/"))
#     answer_ids = {}
#     for answer in answers:
#         answer_ids[answer['id']] = [data_manager.check_file('static/image_for_answer' + str(answer['id']) + '.png'), '/static/image_for_answer' + str(answer['id']) + '.png']
#     return render_template('question.html', question=question, headers_q=headers_q, answers=answers,
#                            headers_a=headers_a, image_q=image_q, filename_q=filename_q, answer_ids=answer_ids)
#
# @app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
# def post_answer(question_id):
#     if request.method == 'GET':
#         single_question = data_manager.get_ordered_dict_by_id('data/question.csv', int(question_id))
#         question_title = single_question['title']
#         return render_template('post-answer.html', question_title=question_title)
#     elif request.method == 'POST':
#         form_answer = request.form['answer_message']
#         data_manager.add_answer(question_id, form_answer)
#         return redirect('/question/{}'.format(question_id))
#
#
# @app.route('/question/<int:question_id>/add-image', methods=['GET', 'POST'])
# def add_image(question_id):
#     if request.method == 'GET':
#         return render_template('add-image.html', question_id=question_id)
#     elif request.method == 'POST':
#         url = request.form['URL']
#         filename = 'static/image_for_question' + str(question_id) + '.png'
#         data_manager.save_image_to_file(url, filename)
#         data_manager.update_line_from_csv("data/question.csv", question_id, 'image', filename)
#         return redirect('/question/{}'.format(question_id))
#
#
# @app.route('/question/<int:question_id>/<int:answer_id>/add-image', methods=['GET', 'POST'])
# def add_image_a(question_id, answer_id):
#     if request.method == 'GET':
#         return render_template('add-image.html')
#     elif request.method == 'POST':
#         url = request.form['URL']
#         filename = 'static/image_for_answer' + str(answer_id) + '.png'
#         data_manager.save_image_to_file(url, filename)
#         data_manager.update_line_from_csv("data/answer.csv", answer_id, 'image', filename)
#         return redirect('/question/{}'.format(question_id))
#
#
# @app.route('/add-question', methods=['GET', 'POST'])
# @app.route('/add-question/<int:question_id>', methods=['GET', 'POST'])
# def add_edit_question(question_id=-1):
#     if question_id >= 0 and request.method == 'GET':
#         question = data_manager.get_ordered_dict_by_id("data/question.csv", question_id)
#         return render_template('add_questions.html', question=question, question_id=question_id)
#
#     elif request.method == 'POST' and question_id >= 0:
#         title = request.form['question_title']
#         message = request.form['question_message']
#         data_manager.edit_line_from_csv('data/question.csv', question_id, title, message)
#         return redirect('/')
#
#     elif request.method == 'GET':
#         return render_template('add_questions.html', question_id=question_id)
#
#     else:
#         data_manager.add_question(request.form['question_title'], request.form['question'])
#         question_id = util.get_id("data/question.csv") -1
#         return redirect('/question/{}'.format(question_id))
#
#
# @app.route('/answer/<answer_id>/delete')
# def delete_answer(answer_id=None):
#     question_id = data_manager.get_key_by_id('data/answer.csv', 'question_id', answer_id)
#     data_manager.delete_line_from_csv('data/answer.csv', answer_id)
#     filename = 'static/image_for_answer' + str(answer_id) + '.png'
#     data_manager.delete_file(filename)
#     return redirect('/question/{}'.format(question_id))
#
#
# @app.route('/question/<int:question_id>/delete-image')
# def delete_question_image(question_id):
#     filename = 'static/image_for_question' + str(question_id) + '.png'
#     data_manager.delete_file(filename)
#     return redirect('/question/{}'.format(question_id))
#
#
# @app.route('/question/<int:question_id>/<int:answer_id>/delete-image')
# def delete_answer_image(question_id, answer_id):
#     filename = 'static/image_for_answer' + str(answer_id) + '.png'
#     data_manager.delete_file(filename)
#     return redirect('/question/{}'.format(question_id))
#
#
# @app.route('/question/<int:question_id>/delete')
# def delete_question(question_id=None):
#     data_manager.delete_line_from_csv('data/question.csv', question_id)
#     filename = 'static/image_for_question' + str(question_id) + '.png'
#     data_manager.delete_file(filename)
#     answers_to_delete = data_manager.get_list_by_key('data/answer.csv', question_id, 'question_id')
#     answers_to_remain = data_manager.get_list_by_not_key('data/answer.csv', question_id, 'question_id')
#     connection.export_csv('data/answer.csv', answers_to_remain)
#
#     for answer in answers_to_delete:
#         print(answer['id'])
#         filename = 'static/image_for_answer' + str(answer['id']) + '.png'
#         data_manager.delete_file(filename)
#     return redirect('/list')
#
#
# @app.route('/question/<int:question_id>/<int:id>/<file_>/<method>')
# def vote(question_id=None, id=None, file_=None, method=None):
#     if file_ == 'answer':
#         data_manager.change_vote_number_in_csv('data/answer.csv', id, method)
#     else:
#         data_manager.change_vote_number_in_csv('data/question.csv', id, method)
#     return redirect('/question/{}'.format(question_id))
#
#
# if __name__ == '__main__':
#     app.run(debug=True, port=5000, host='0.0.0.0')
