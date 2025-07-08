from random import choice

question_type = ["input", "range"]

questions = ["what is your favorite color?", "how do you feel your favorite color/s", "what do you hate the most?"]

next_prompts = ["how many", "how many times", "how many times are"]


def simulate_ai_request(t: str, **kwargs):
    if t == "q":
        return {"type": choice(question_type), "question": choice(questions)}
    elif t == "a":
        return choice(next_prompts)
