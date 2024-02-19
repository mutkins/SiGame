import json
from tools import get_question_by_id, configure_questions, mark_question_as_answered
from flask import Flask, render_template, request
from Team import Team

app = Flask(__name__)
global pack
with open('pack.json', 'r', encoding='utf-8') as file:
    pack = json.load(file)

pack = configure_questions(pack)

team1 = Team('ЗУБОЗАВРЫ')
team2 = Team('ЗАТОЧЕННЫЕ ЗАБРОЗУБЫ')


@app.route('/', methods=['GET'])
def round_menu():
    return render_template('regular_round.html', themes=pack[0].get('themes'))


@app.route('/', methods=['POST'])
def round_menu1():
    global pack
    a = request
    question_id = request.form.get('id').replace('/', '')
    pack = mark_question_as_answered(pack=pack, question_id=question_id)
    with open('pack1.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(pack))
    return render_template('regular_round.html', themes=pack[0].get('themes'))


@app.route('/q', methods=['GET'])
def show_question():
    question_id = request.args.get('id').replace('/', '')
    question = get_question_by_id(pack=pack, question_id=question_id)
    return render_template('question.html', question=question)


@app.route('/q', methods=['POST'])
def show_question2():
    a = request
    question_id = request.form.get('id').replace('/', '')
    question = get_question_by_id(pack=pack, question_id=question_id)
    return render_template('question.html', question=question, ft_result=ft_result, st_result=st_result)


if __name__ == '__main__':
    app.run()