import random


def get_question_by_id(pack, question_id):
    for round in pack:
            for theme in round.get("themes"):
                    for question in theme.get("questions"):
                        if question.get("id") == int(question_id):
                            return question


def configure_questions(pack):
    for round in pack:
        for theme in round.get("themes"):
            for question in theme.get("questions"):
                question["id"] = random.randint(0, 100000)
                question["answered"] = False
    return pack


def mark_question_as_answered(pack, question_id):
    for round in pack:
        for theme in round.get("themes"):
            for question in theme.get("questions"):
                if question.get("id") == int(question_id):
                    # del pack[pack.index(round)].get("themes")[round.get("themes").index(theme)].get("questions")[
                    #     theme.get("questions").index(question)]
                    question["answered"] = True
                    return pack
