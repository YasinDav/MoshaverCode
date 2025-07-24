from random import choice

question_type = ["input", "range"]

questions = ["what is your favorite color?", "how do you feel your favorite color/s", "what do you hate the most?"]

next_prompts = ["how many", "how many times", "how many times are"]


def simulate_ai_request(t: str, **kwargs):
    if t == "q":
        return {"type": choice(question_type), "question": choice(questions)}
    elif t == "a":
        return choice(next_prompts)


# import httpx
#
# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL = "mistral:latest"
# TIMEOUT = 60.0
#
#
# def simulate_ai_request(t: str, *, prompt: str = None, user_input: str = None):
#     """
#     t == "q": prompt را می‌گیرد و بر اساس آن یک سؤال جدید برمی‌گرداند.
#     t == "a": user_input را می‌گیرد و بر اساس آن next_prompt برمی‌گرداند.
#     """
#     # پایه history
#     messages = [{
#         "role": "system",
#         "content": (
#             "شما یک مشاور علمی-روانشناسی هستید. "
#             "برای هر مرحله:"
#             " اگر t='q' باشد، با توجه به prompt یک سؤال جدید بپرس؛"
#             " اگر t='a' باشد، با توجه به پاسخ کاربر یک next_prompt کوتاه بساز."
#         )
#     }]
#
#     if t == "q":
#         if not prompt:
#             raise ValueError("برای t='q' باید prompt بدهید")
#         messages.append({"role": "user", "content": prompt})
#
#     elif t == "a":
#         if user_input is None:
#             raise ValueError("برای t='a' باید user_input بدهید")
#         messages.append({"role": "user", "content": f"Answer: {user_input}"})
#         messages.append({"role": "user", "content":
#             "با توجه به این پاسخ، یک next_prompt کوتاه برای سؤال بعدی بده."})
#     else:
#         raise ValueError("t باید 'q' یا 'a' باشد")
#
#     payload = {"model": MODEL, "messages": messages, "stream": False}
#     with httpx.Client(timeout=TIMEOUT) as client:
#         resp = client.post(OLLAMA_URL, json=payload)
#         resp.raise_for_status()
#         ai_text = resp.json()["message"]["content"].strip()
#
#     if t == "q":
#         return {"type": "input", "question": ai_text}
#     else:
#         return ai_text
#
#
# simulate_ai_request(t="q", prompt="ask about user feel.")
# import requests
#
# response = requests.post(
#     'http://localhost:11500/api/generate',
#     json={
#         'model': 'mistral',
#         'prompt': f"کاربر: {"من خیلی به هنر علاقه مندم"}\nدستیار:",
#         'stream': False
#     }
# )
#
# print(response.json())
