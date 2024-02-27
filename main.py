import json
from tools import get_question_by_id, configure_questions, mark_question_as_answered, add_score, configure_players, get_current_round_table, mark_round_as_started
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


@app.route('/', methods=['GET'])
def render_round_table():
    global pack
    result = get_current_round_table(pack=pack)
    match  result.get("type"):
        case "themes_list": return render_theme_list(result.get("round"))
        case "round_table": return render_template('regular_round.html', round=result.get("round"), players=players)
        case "intuition": return render_template('intuition.html', round=result.get("round"), players=players)


def render_theme_list(round):
    return render_template('themes_list.html', round=round)


@app.route('/', methods=['POST'])
def post_answered():
    global pack
    global players
    a = request
    question_id = None
    for item in request.form:
        if item.startswith('id'):
            question_id = request.form.get(item).replace('/', '')
        if item.startswith('player'):
            score = request.form.get(item).replace('/', '')
            players = add_score(players=players, player_id=item, score=score)
    if question_id:
        pack = mark_question_as_answered(pack=pack, question_id=question_id)
    return render_round_table()


@app.route('/start_round', methods=['POST'])
def start_round():
    global pack
    round_num = request.form.get('round_num').replace('/', '')
    pack = mark_round_as_started(pack=pack, round_num=round_num)
    a = pack
    return render_round_table()


@app.route('/q', methods=['GET'])
def show_question():
    question_id = request.args.get('id').replace('/', '')
    question = get_question_by_id(pack=pack, question_id=question_id)
    if question.get("type") == "intuition":
        return render_template('intuition_question.html', question=question, players=players)
    else:
        return render_template('question.html', question=question, players=players)


# @app.route('/q', methods=['POST'])
# def show_question2():
#     question_id = request.form.get('id').replace('/', '')
#     question = get_question_by_id(pack=pack, question_id=question_id)
#     return render_template('question.html', question=question, players=players)


if __name__ == '__main__':
    app.run()
