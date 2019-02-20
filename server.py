from flask import Flask, request, render_template, redirect
import util
import time
import connection
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_index():
    questions = connection.import_csv('data/question.csv')
    header = util.get_headers('data/question.csv')[4]

    return render_template('index.html', questions=questions, header=header)


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
        single_question = data_manager.get_ordered_dict_by_id('data/question.csv', int(question_id))
        question_message = single_question['message']
        return render_template('post-answer.html', question_message=question_message)
    elif request.method == 'POST':
        form_answer = request.form['answer_message']
        data_manager.new_answer(question_id, form_answer)
        return redirect('/question/<int:question_id>')


@app.route('/add-question', methods=['GET', 'POST'])
def add_new_question():
    if request.method == 'GET':
        return render_template('add_questions.html')
    else:
        data_manager.new_question(request.form['question_title'], request.form['question'])
        question_id = util.get_id("data/question.csv")
        return redirect('/question/{}'.format(question_id))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id=None):
    data_manager.delete_answer_from_csv(answer_id)
    return redirect('/add-question')


@app.route('/answer/<question_id>/delete')
def delete_question(question_id=None):
    data_manager.delete_question_from_csv(question_id)
    return redirect('/add-question')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')