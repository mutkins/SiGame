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
        round["state"] = None
    return pack


def mark_question_as_answered(pack, question_id):
    for round in pack:
        for theme in round.get("themes"):
            for question in theme.get("questions"):
                if question.get("id") == question_id:
                    question["answered"] = True
                    round["state"] = "in_progress"
                    pack = mark_round_as_finished(pack=pack)
                    return pack


def mark_round_as_finished(pack):
    for round in pack:
        for theme in round.get("themes"):
            for question in theme.get("questions"):
                if not question["answered"]:
                    return pack
        round["state"] = "finished"
    return pack


def is_need_to_show_welcome(pack):
    for round in pack:
        if round["state"] is None:
            print()
            return round
        if round["state"] is None and pack[pack.index(round)-1]["state"] == "finished":
            print()
            return round




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
