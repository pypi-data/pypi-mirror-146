import json
import os.path
import random

FILEPATH = os.path.join(os.path.dirname(__file__), "resources", "babbles.json")


def spout() -> str:
    with open(FILEPATH, "r") as file:
        data = json.load(file)
    return random.choice(data)


def spout_softly() -> str:
    return spout().lower()
