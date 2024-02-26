import json
from tools import get_question_by_id, configure_questions, mark_question_as_answered, add_score, configure_players
from flask import Flask, render_template, request
from Players import Players

app = Flask(__name__)

global pack
with open('pack.json', 'r', encoding='utf-8') as file:
    pack = json.load(file)

pack = configure_questions(pack)

player_1 = Players('ЗУБОЗАВРЫ')
player_2 = Players('ЗАТОЧЕННЫЕ ЗАБРОЗУБЫ')
players = [player_1, player_2]

players = configure_players(players)
print()
@app.route('/', methods=['GET'])
def round_menu():
    global players
    return render_template('regular_round.html', pack=pack, players=players)


@app.route('/', methods=['POST'])
def round_menu1():
    global pack
    global players
    for item in request.form:
        if item.startswith('id'):
            question_id = request.form.get(item).replace('/', '')
        if item.startswith('player'):
            score = request.form.get(item).replace('/', '')
            players = add_score(players=players, player_id=item, score=score)
    pack = mark_question_as_answered(pack=pack, question_id=question_id)
    return render_template('regular_round.html', pack=pack, players=players)


@app.route('/q', methods=['GET'])
def show_question():
    question_id = request.args.get('id').replace('/', '')
    question = get_question_by_id(pack=pack, question_id=question_id)
    return render_template('question.html', question=question, players=players)


@app.route('/q', methods=['POST'])
def show_question2():
    question_id = request.form.get('id').replace('/', '')
    question = get_question_by_id(pack=pack, question_id=question_id)
    return render_template('question.html', question=question, players=players)


if __name__ == '__main__':
    app.run()
