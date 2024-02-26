import random


def get_question_by_id(pack, question_id):
    for round in pack:
            for theme in round.get("themes"):
                    for question in theme.get("questions"):
                        if question.get("id") == question_id:
                            return question


def configure_questions(pack):
    for round in pack:
        for theme in round.get("themes"):
            for question in theme.get("questions"):
                question["id"] = "question" + str(random.randint(0, 1000000))
                question["answered"] = False
        round["answered"] = False
    return pack


def mark_question_as_answered(pack, question_id):
    for round in pack:
        for theme in round.get("themes"):
            for question in theme.get("questions"):
                if question.get("id") == question_id:
                    question["answered"] = True
                    pack = mark_round_as_answered(pack=pack)
                    return pack


def mark_round_as_answered(pack):
    for round in pack:
        for theme in round.get("themes"):
            for question in theme.get("questions"):
                if not question["answered"]:
                    return pack
        round["answered"] = True
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
            player.name = player.name[:12]+'...'
    return players
