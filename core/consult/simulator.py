import httpx

OLLAMA_URL = "http://192.168.80.1:11500/api/chat"
MODEL = "mistral:latest"
TIMEOUT = 120.0

# first prompt
first_prompt = "it's first question about user. you have to begin asking. for start, ask interesting and general questions. and also just ask one question."


def ai_request(t: str, *, prompt: str = None, user_input: str = None, question: str = None):
    # پایه history
    messages_q = [
        {"role": "system",
         "content": (
             "شما یک مشاور علمی-روانشناسی برای تشخیص روحیات و شخصیت کاربر هستید. و قصد دارید به در انتخاب شغل کمک کنید. "
             "برای هر مرحله:"
             "با توجه به پرامپت ،فقط یک سوال فارسی برای درک سلایق و رفتار کاربر بپرس. همچنین فقط متن سوال بدون الاعم خاص یا هیچی ادامه ایی تاکیید میکنم فقط متن سوال بدون توضیح و در سوال از پرانتز استفاده نکن."
             "user just can answer by two way, \"input\" that sends to you a text message . \"range\" that send a range of feelings 'very bad' 'bad' 'neutral' 'very' 'very much' .you have to choose one of them; give me one word , \"input\" or \"range\".use this format:(input/range)\n\n(Persian Question here)"
         )
         }]

    messages_a = [
        {"role": "system",
         "content": (
             "شما یک مشاور علمی-روانشناسی برای تشخیص روحیات و شخصیت کاربر هستید. و قصد دارید به در انتخاب شغل کمک کنید. "
             "برای هر مرحله:"
             "با توجه به سوالی که تو قبلا از کاربر پرسیدی ، و جوابی که کاربر داده است ، یک پرامپت به من بده. این پرامپت جهت تولید سوال بعدی از کاربر استفاده میشود. پس سولات و کجهولاتی که از کاربر داری را توضیح بده. ولی فقط درباره یک موضوع واحد و مشخص بپرس. "

         )
         }]

    if t == "q":
        if not prompt:
            raise ValueError("برای t='q' باید prompt بدهید")
        messages_q.append({"role": "user", "content": prompt})
        messages = messages_q


    elif t == "a":
        if user_input is None or question is None:
            raise ValueError("برای t='a' باید user_input بدهید")
        messages_a.append({"role": "system", "content": f"you asked a question\nQuestion: \"{question}\""})
        messages_a.append({"role": "user", "content": f"Answer: {user_input}"})
        messages_a.append({"role": "user",
                           "content": "جواب کاربر را برسی کن. برای شناخت کاربر یک پرامپت تواید کن که برای ساخت سوال بعدی از کاربر استفاده خواهد شد"})
        messages = messages_a
    else:
        raise ValueError("t باید 'q' یا 'a' باشد")

    payload = {"model": MODEL, "messages": messages, "stream": False}
    with httpx.Client(timeout=TIMEOUT) as client:
        resp = client.post(OLLAMA_URL, json=payload)
        resp.raise_for_status()
        ai_text = resp.json()

    if t == "q":
        response = str(ai_text["message"]["content"])
        type = None
        if response.find("(input)") != -1 or response.startswith(" (input)"):
            type = "input"
            response = response.replace("input", "")
        if response.find("(range)") != -1 or response.startswith(" (range)"):
            type = "range"
            response = response.replace("range", "")
        response = response.replace("(", "").replace(")", "")
        # result = GoogleTranslator(source='auto', target='fa').translate(response)

        return {"type": type, "question": response}
    else:
        return str(ai_text["message"]["content"])


def ai_request_result():
    messages = [
        {"role": "system",
         "content": (
             "شما یک مشاور علمی-روانشناسی برای تشخیص روحیات و شخصیت کاربر هستید. و قصد دارید به در انتخاب شغل کمک کنید. "
             "برای هر مرحله:"
             "به تمام مکالمات توجه کن و شیخصیت کاربر را تشخیص بده. شغل مناسب او چیست ؟ و نقات قوت و ضعف او را شرح بده"
         )
         }]
    payload = {"model": MODEL, "messages": messages, "stream": False}
    with httpx.Client(timeout=TIMEOUT) as client:
        resp = client.post(OLLAMA_URL, json=payload)
        resp.raise_for_status()
        ai_text = resp.json()

    return str(ai_text["message"]["content"])


def ai_request_percentage(ai_text):
    messages = [
        {"role": "system",
         "content": (
             "شما یک مشاور علمی-روانشناسی برای تشخیص روحیات و شخصیت کاربر هستید. و قصد دارید به در انتخاب شغل کمک کنید. "
             "برای هر مرحله:"
             f"rate user's {ai_text} from 0 to 100 percent. just give me number without any character"
         )
         }]
    payload = {"model": MODEL, "messages": messages, "stream": False}
    with httpx.Client(timeout=TIMEOUT) as client:
        resp = client.post(OLLAMA_URL, json=payload)
        resp.raise_for_status()
        ai_text = resp.json()
    percent = str(ai_text["message"]["content"])
    result = ""
    for i in percent:
        if i.isnumeric():
            result += i

    result = int(result)

    return result
