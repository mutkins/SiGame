import json
from tools import get_question_by_id, configure_questions, mark_question_as_answered, add_score, configure_players, is_there_questions_in_round, mark_round_as_started, get_round_by_num, get_current_round_num
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
def render_welcome_page():
    return render_template('welcome_page.html')


@app.route('/themes', methods=['GET'])
def render_theme_list(round_num=None):
    global pack
    if not round_num:
        round_num = request.args.get('round_num').replace('/', '')
    round = get_round_by_num(pack=pack, round_num=round_num)
    return render_template('themes_list.html', round=round)


@app.route('/start_round', methods=['GET'])
def start_round():
    global pack
    round_num = request.args.get('round_num').replace('/', '')
    pack = mark_round_as_started(pack=pack, round_num=round_num)
    return render_round_table(round_num=round_num)


@app.route('/round_table', methods=['GET'])
def render_round_table(round_num=None):
    global pack
    if not round_num:
        if not request.args.get('round_num'):
            round_num = get_current_round_num(pack=pack)
        else:
            round_num = request.args.get('round_num').replace('/', '')
    round = get_round_by_num(pack=pack, round_num=round_num)
    match  round.get("type"):
        case "regular": return render_template('regular_round.html', round=round, players=players)
        case "intuition": return render_template('intuition.html', round=round, players=players)


@app.route('/question', methods=['GET'])
def show_question():
    global pack
    question_id = request.args.get('question_id').replace('/', '')
    question = get_question_by_id(pack=pack, question_id=question_id)
    round_num = request.args.get('round_num').replace('/', '')
    match question.get("type"):
        case "intuition": return render_template('intuition_question.html', question=question, players=players, round_num=round_num)
        case _: return render_template('question.html', question=question, players=players, round_num=round_num)


@app.route('/round_table', methods=['POST'])
def post_answered():
    global pack
    global players
    answered_question_id = None
    round_num = request.form.get("round_num").replace('/', '')
    for item in request.form:
        if item.startswith('question_id'):
            answered_question_id = request.form.get(item).replace('/', '')
        if item.startswith('player'):
            score = request.form.get(item).replace('/', '')
            players = add_score(players=players, player_id=item, score=score)
    if answered_question_id:
        pack = mark_question_as_answered(pack=pack, question_id=answered_question_id)
    if is_there_questions_in_round(pack=pack, round_num=round_num):
        return render_round_table(round_num=round_num)
    else:
        return render_theme_list(round_num=int(round_num)+1)




# @app.route('/', methods=['GET'])
# def render_round_table():
#     global pack
#     result = get_current_round_table(pack=pack)
#     match  result.get("type"):
#         case "themes_list": return render_theme_list(result.get("round"))
#         case "round_table": return render_template('regular_round.html', round=result.get("round"), players=players)
#         case "intuition": return render_template('intuition.html', round=result.get("round"), players=players)




#
# @app.route('/questions', methods=['GET'])
# def render_theme_list():
#     round_num = request.args.get('round_num').replace('/', '')
#     return render_template('themes_list.html', round=round)

# @app.route('/', methods=['POST'])
# def post_answered():
#     global pack
#     global players
#     a = request
#     question_id = None
#     for item in request.form:
#         if item.startswith('id'):
#             question_id = request.form.get(item).replace('/', '')
#         if item.startswith('player'):
#             score = request.form.get(item).replace('/', '')
#             players = add_score(players=players, player_id=item, score=score)
#     if question_id:
#         pack = mark_question_as_answered(pack=pack, question_id=question_id)
#     return render_round_table()


# @app.route('/start_round', methods=['POST'])
# def start_round():
#     global pack
#     round_num = request.form.get('round_num').replace('/', '')
#     pack = mark_round_as_started(pack=pack, round_num=round_num)
#     a = pack
#     return render_round_table()


# @app.route('/q', methods=['GET'])
# def show_question():
#     question_id = request.args.get('id').replace('/', '')
#     question = get_question_by_id(pack=pack, question_id=question_id)
#     if question.get("type") == "intuition":
#         return render_template('intuition_question.html', question=question, players=players)
#     else:
#         return render_template('question.html', question=question, players=players)


# @app.route('/q', methods=['POST'])
# def show_question2():
#     question_id = request.form.get('id').replace('/', '')
#     question = get_question_by_id(pack=pack, question_id=question_id)
#     return render_template('question.html', question=question, players=players)


if __name__ == '__main__':
    app.run()
