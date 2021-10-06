import json


def get_json(fn):
    with open(fn, "r") as f:
        return json.load(f)