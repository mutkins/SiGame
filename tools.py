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

                    pack = mark_round_as_finished(pack=pack)
                    return pack


def mark_round_as_started(pack, round_num):
    for round in pack:
        if round.get("round_num") == int(round_num):
            round["state"] = "in_progress"
    return pack


def mark_round_as_finished(pack):
    for round in pack:
        for theme in round.get("themes"):
            for question in theme.get("questions"):
                if not question["answered"]:
                    return pack
        round["state"] = "finished"
    return pack


def get_current_round_table(pack):
    for round in pack:
        if round["state"] is None:
            return {"type": "themes_list", "round": round}
        elif round["state"] == "in_progress":
            return {"type": "regular", "round": round}
        else:
            continue
    return None


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
