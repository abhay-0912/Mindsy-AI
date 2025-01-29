from random import choice

EXPRESSIONS = {
    "greeting": ["smile", "wave"],
    "help": ["thinking", "curious"],
    "weather": ["neutral", "checking"],
    "joke": ["laughing", "grinning"],
    "news": ["serious", "focused"],
    "task_execution": ["determined", "working"],
    "farewell": ["waving", "neutral"],
    "error": ["confused", "shrug"]
}

def get_expression(intent):
    return choice(EXPRESSIONS.get(intent, ["neutral"]))
