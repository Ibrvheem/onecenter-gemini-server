import random
import time

def get_waiting_response(should_sleep=False):
    """
    The function returns a random response while a user waits for a long
    request to be completed by an AI customer agent.
    """
    responses = [
        "Please bear with me while I find a fitting answer for you.",
        "Ok, I am trying to find an answer for you.",
        "I'm looking through the manual to get an answer for you.",
        "Please hold while I find an answer for your query",
    ]
    if should_sleep:
        time.sleep(3)
    return random.choice(responses)