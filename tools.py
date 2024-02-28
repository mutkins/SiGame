import random


def get_question_by_id(pack, question_id):
    for round in pack:
        for theme in round.get("themes"):
            for question in theme.get("questions"):
                if question.get("id") == question_id:
                    return question


def configure_questions(pack):
    for index, round in enumerate(pack, start=1):
        round["round_num"] = index
        for theme in round.get("themes"):
            for question in theme.get("questions"):
                question["id"] = "question" + str(random.randint(0, 1000000))
                question["answered"] = False
    return pack


def mark_question_as_answered(pack, question_id):
    for round in pack:
        for theme in round.get("themes"):
            for question in theme.get("questions"):
                if question.get("id") == question_id:
                    question["answered"] = True
                    return pack


def add_score(players, player_id, score):
    score = int(score)
    for player in players:
        if player.id == player_id:
            player.score += score
    return players


def configure_players(players):
    for player in players:
        if len(player.name) > 12:
            player.name = player.name[:12] + '...'
    return players


def get_round_by_num(pack, round_num):
    for round in pack:
        if round.get("round_num") == int(round_num):
            return round
    return None


def is_there_questions_in_round(pack, round_num):
    round = get_round_by_num(pack=pack, round_num=round_num)
    for theme in round.get("themes"):
        for question in theme.get("questions"):
            if not question["answered"]:
                return True
    return False