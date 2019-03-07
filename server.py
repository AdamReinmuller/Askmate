from flask import Flask, request, render_template, redirect
import util
import data_manager

app = Flask(__name__)


@app.route('/')
def index():
    questions = data_manager.sort_table(data_manager.question_db, 'id', 'desc')
    header = data_manager.get_column_names_of_table(data_manager.question_db)[4]
    return render_template('index.html', questions=questions, header=header)


@app.route('/list')
@app.route('/list/')
def route_list():
    questions = data_manager.import_from_db(data_manager.question_db)
    headers = data_manager.get_column_names_of_table(data_manager.question_db)
    if request.args:
        questions = data_manager.sort_table(data_manager.question_db, request.args['order_by'],
                                            request.args['order_direction'])
    return render_template('list.html', questions=questions, headers=headers)


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id, comment=None, comment_id=-1):
    if request.method == 'GET':
        question_title = data_manager.get_line_data_by_id('question', question_id)[0]['title']
        return render_template('comment.html', question_title=question_title, comment=comment, comment_id=comment_id)

    elif request.method == 'POST':
        data_manager.add_comment_to_table('comment', 'question_id', question_id, request.form['comment'], util.get_time(), 0)
        return redirect('/question/{}'.format(question_id))


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id, comment=None, comment_id=-1):
    if request.method == 'GET':
        answer_message = data_manager.get_line_data_by_id('answer', answer_id)[0]['message']
        return render_template('comment.html', answer_id=answer_id, answer_message=answer_message, comment=comment, comment_id=comment_id)

    elif request.method == 'POST':
        question_id = data_manager.get_foreign_key_by_id('answer', 'question_id', answer_id)[0]['question_id']
        data_manager.add_comment_to_table('comment', 'answer_id', answer_id, request.form['comment'], util.get_time(), 0)
        return redirect('/question/{}'.format(question_id))

@app.route('/comments/<int:comment_id>/delete')
def delete_comment(comment_id):
    answer_id = data_manager.get_foreign_key_by_id('comment', 'answer_id', comment_id)[0]['answer_id']
    if answer_id:
        question_id = data_manager.get_foreign_key_by_id('answer', 'question_id', answer_id)[0]['question_id']
    else:
        question_id = data_manager.get_foreign_key_by_id('comment', 'question_id', comment_id)[0]['question_id']
    data_manager.delete_line_by_id('comment', comment_id)
    return redirect('/question/{}'.format(question_id))


@app.route('/comments/<int:comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    if request.method == 'GET':
        comment = data_manager.get_line_data_by_id('comment', comment_id)
        return render_template('comment.html', comment_id= comment_id, comment=comment)

    elif request.method == 'POST':
        answer_id = data_manager.get_foreign_key_by_id('comment', 'answer_id', comment_id)[0]['answer_id']
        if answer_id:
            question_id = data_manager.get_foreign_key_by_id('answer', 'question_id', answer_id)[0]['question_id']
        else:
            question_id = data_manager.get_foreign_key_by_id('comment', 'question_id', comment_id)[0]['question_id']
        data_manager.update_comment_message_submt_editedc_by_id(comment_id, request.form['comment'], util.get_time())
        return redirect('/question/{}'.format(question_id))


@app.route('/question/<int:question_id>')
def route_question(question_id):
    question = data_manager.get_line_data_by_id('question', question_id)
    headers_q = data_manager.get_headers('question')
    headers_c = list(data_manager.get_headers('comment'))[3:5]
    headers_a = data_manager.get_headers('answer')
    comments_q = data_manager.get_comments_data_by_foreign_id('question_id', question_id)
    answers = data_manager.get_lines_data_by_foreign_id('answer', 'question_id', question_id)
    filename_q = '/static/image_for_question' + str(question_id) + '.png'
    image_q = util.check_file(filename_q.lstrip("/"))
    answer_ids = {}
    for answer in answers:
        answer_ids[answer['id']] = [util.check_file('static/image_for_answer' + str(answer['id']) + '.png'),
                                              '/static/image_for_answer' + str(answer['id']) + '.png',
                                                data_manager.get_lines_data_by_foreign_id('comment', 'answer_id', answer['id'])]
    return render_template('question.html', question_id=question_id, question=question, headers_q=headers_q,
                           comments_q=comments_q, headers_c=headers_c, answers=answers,
                           headers_a=headers_a, image_q=image_q, filename_q=filename_q, answer_ids=answer_ids)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'GET':
        single_question = data_manager.get_line_data_by_id(data_manager.question_db, question_id)
        question_title = single_question[0]['title']
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
        return redirect('/question/{}'.format(question_id))

    elif request.method == 'GET':
        return render_template('add_questions.html', question_id=question_id)

    else:
        data_manager.add_question(request.form['question_title'], request.form['question'])
        question_id = util.get_last_question_id()
        return redirect('/question/{}'.format(question_id))


@app.route('/question/<int:question_id>/add-tag', methods=['GET', 'POST'])
def add_tag_to_question(question_id=None):
    if request.method == 'GET':
        question = data_manager.get_question_by_id(question_id)
        question_title = question[0]['title']
        tag = util.get_tag(question_id)
        return render_template('add_tag.html', question_title=question_title, tag=tag, question_id=question_id)
    else:
        question = data_manager.get_question_by_id(question_id)
        question_id_to_add = question[0]['id']
        tag = request.form['new_tag']
        data_manager.add_tag_to_question(question_id_to_add, tag)
        return redirect('/question/{}'.format(question_id))


@app.route('/question/<int:question_id>/delete-tag')
def delete_tag(question_id=None):
    try:
        data_manager.delete_tag(question_id)
    except:
        pass
    finally:
        return redirect('/question/{}'.format(question_id))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id=None):
    data_manager.delete_line_by_foreign_id(data_manager.comment_db, 'answer_id', answer_id)
    question_id = data_manager.delete_answer_by_id(answer_id)['question_id']
    return redirect('/question/{}'.format(question_id))


@app.route('/question/<int:question_id>/delete')
def delete_question(question_id=None):
    data_manager.delete_line_by_id('comment', question_id)
    filename = 'static/image_for_question' + str(question_id) + '.png'
    util.delete_file(filename)
    answer_ids_to_delete = data_manager.get_ids_by_foreign_id(data_manager.answer_db, 'question_id', question_id)
    print(answer_ids_to_delete)
    for answer_id in answer_ids_to_delete:
        data_manager.delete_line_by_foreign_id(data_manager.comment_db, 'answer_id', answer_id['id'])
        filename = 'static/image_for_answer' + str(answer_id['id']) + '.png'
        util.delete_file(filename)
    data_manager.delete_answer_by_question_id(question_id)
    data_manager.delete_question(question_id)
    return redirect('/list')



@app.route('/question/<int:question_id>/<int:id>/<file_>/<method>')
def vote(question_id=None, id=None, file_=None, method=None):
    if file_ == 'answer':
        data_manager.change_vote_number_in_table('data/answer.csv', id, method)
    else:
        data_manager.change_vote_number_in_table('data/question.csv', id, method)
    return redirect('/question/{}'.format(question_id))


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_phrase = request.form['search_phrase']
    headers = data_manager.get_column_names_of_table(data_manager.question_db)
    questions = data_manager.search(search_phrase)
    answers = data_manager.search_answers(search_phrase)
    return render_template('search_results.html', questions=questions, answers=answers, headers=headers)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
