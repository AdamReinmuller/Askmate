from flask import Flask, request, render_template, redirect
import util
import time
import connection
import data_manager

app = Flask(__name__)


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
def delete_answer(question_id=None):
    data_manager.delete_question_from_csv(question_id)
    return redirect('/add-question')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
