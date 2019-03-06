from flask import Flask, request, render_template, redirect
import util
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
@app.route('/list/')
def route_list():
    questions = data_manager.import_from_db(data_manager.question_db)
    headers = data_manager.get_column_names_of_table(data_manager.question_db)
    if request.args:
        questions = data_manager.sort_table(data_manager.question_db, request.args['order_by'],
                                            request.args['order_direction'])
    return render_template('list.html', questions=questions, headers=headers)


@app.route('/question/<int:question_id>')
def route_question(question_id):
    question = data_manager.get_ordered_dict_by_id('data/question.csv', question_id)
    headers_q = util.get_headers('data/question.csv')
    answers = data_manager.get_list_by_key('data/answer.csv', question_id, 'question_id')
    headers_a = util.get_headers('data/answer.csv')
    return render_template('question.html', question=question, headers_q=headers_q, answers=answers,
                           headers_a=headers_a)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'GET':
        single_question = data_manager.get_ordered_dict_by_id(data_manager.answer_db, int(question_id))
        question_title = single_question['title']
        return render_template('post-answer.html', question_title=question_title)
    elif request.method == 'POST':
        form_answer = request.form['answer_message']
        data_manager.add_answer(question_id, form_answer)
        return redirect('/question/{}'.format(question_id))


@app.route('/add-question', methods=['GET', 'POST'])
@app.route('/add-question/<int:question_id>', methods=['GET', 'POST'])
def add_edit_question(question_id=None):
    if question_id and request.method == 'GET':
        question = data_manager.get_ordered_dict_by_id(data_manager.question_db, int(question_id))
        return render_template('add_questions.html', question=question, question_id=question_id)

    elif request.method == 'POST' and question_id:
        title = request.form['question_title']
        message = request.form['question_message']
        data_manager.update_question(question_id, title, message)
        return redirect('/')

    elif request.method == 'GET':
        return render_template('add_questions.html', question_id=question_id)

    else:
        data_manager.add_question(request.form['question_title'], request.form['question'])
        question_id = util.get_last_question_id()
        return redirect('/question/{}'.format(question_id))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id=None):
    question_id = data_manager.delete_answer(answer_id)
    return redirect('/question/{}'.format(question_id))


@app.route('/question/<int:question_id>/delete')
def delete_question(question_id=None):
    data_manager.delete_question(question_id)
    return redirect('/list')


@app.route('/question/<int:question_id>/<int:id>/<file_>/<method>')
def vote(question_id=None, id=None, file_=None, method=None):
    if file_ == 'answer':
        data_manager.change_vote_number_in_table('data/answer.csv', id, method)
    else:
        data_manager.change_vote_number_in_table('data/question.csv', id, method)
    return redirect('/question/{}'.format(question_id))


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
