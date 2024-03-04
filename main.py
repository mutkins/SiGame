import json
from tools import get_question_by_id, configure_questions, mark_question_as_answered, add_score, configure_players, is_there_questions_in_round, get_round_by_num
from flask import Flask, render_template, request, redirect, url_for
from Players import Players

app = Flask(__name__)

pack = None
players = []


@app.route('/', methods=['GET'])
def render_welcome_page():
    return render_template('welcome_page.html')


@app.route('/game_init', methods=['POST'])
def game_init():
    global pack
    with open('pack.json', 'r', encoding='utf-8') as file:
        pack = json.load(file)
    pack = configure_questions(pack)
    global players
    for item in request.form:
        if item.startswith('player_name'):
            player_name = request.form.get(item).replace('/', '')
            player = Players(player_name)
            players.append(player)
    return redirect(url_for('render_theme_list', round_num=1))


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
    # return render_round_table(round_num=round_num)
    return redirect(url_for('render_round_table', round_num=round_num))


@app.route('/round_table', methods=['GET'])
def render_round_table(round_num=None):
    global pack
    global players
    if not round_num:
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
    # return what_to_do_after_question_answered(pack=pack, round_num=round_num)
    return redirect(url_for('render_round_table', round_num=round_num))


# def what_to_do_after_question_answered(pack, round_num):
#     if is_there_questions_in_round(pack=pack, round_num=round_num):
#         # return render_round_table(round_num=round_num)
#         return redirect(url_for('render_round_table', round_num=round_num))
#     elif get_round_by_num(pack=pack, round_num=int(round_num)+1):
#         # return render_theme_list(round_num=int(round_num)+1)
#         return redirect(url_for('render_theme_list', round_num=int(round_num)+1))
#     else:
#         return redirect(url_for('render_round_table', round_num=round_num))


@app.route('/prev_round', methods=['GET'])
def prev_round():
    round_num = request.args.get('round_num').replace('/', '')
    if get_round_by_num(pack=pack, round_num=int(round_num) - 1):
        return redirect(url_for('render_theme_list', round_num=int(round_num) - 1))
    else:
        return redirect(url_for('render_round_table', round_num=round_num))


@app.route('/next_round', methods=['GET'])
def next_round():

    round_num = request.args.get('round_num').replace('/', '')
    if get_round_by_num(pack=pack, round_num=int(round_num) + 1):
        return redirect(url_for('render_theme_list', round_num=int(round_num) + 1))
    else:
        return redirect(url_for('render_summary'))


@app.route('/summary', methods=['GET'])
def render_summary():
    global players
    return render_template('summary.html', players=players)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
