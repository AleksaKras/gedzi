import time

import telebot
import datetime
from pymongo import MongoClient
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("###", protect_content=True)


class DataBase:
    def __init__(self):
        cluster = MongoClient()
        self.db = cluster[""]
        self.users = self.db["Users"]
        self.questions = self.db["Questions"]

    def get_user(self, chat_id):
        user = self.users.find_one({"chat_id": chat_id})
        today = str(datetime.date.today())
        if user is not None:
            return user

        user = {
            "chat_id": chat_id,
            "is_passing": False,
            "is_passed": False,
            "question_index": None,
            "category": None,
            'vata': False,
            'done': False,
            "answers": [],
            'date': today,
        }
        #print(user)

        self.users.insert_one(user)

        return user

    def set_user(self, chat_id, update):
        self.users.update_one({"chat_id": chat_id}, {"$set": update})

        def get_question(self, index, category):
            # print('ind', index, category)
            return self.questions.find_one({"question": index, "category": category})

    def questions_count(self, category):
        # print('category', category)
        return len(list(self.questions.find({"category": category})))

    def users_count(self):
        return len(list(self.users.find()))

    def vata_count(self):
        return len(list(self.users.find({'vata':True})))

    def day_users_count(self):
        today = str(datetime.date.today())
        return len(list(self.users.find({'date':today})))

    def day_vata_count(self):
        today = str(datetime.date.today())
        return len(list(self.users.find({'vata':True, 'date':today})))




db = DataBase()


@bot.message_handler(commands=["start"])
def start(message):
    user = db.get_user(message.chat.id)

    # checking of second activity
    if user["is_passed"]:
        bot.send_message(message.from_user.id, "Друже, ти вже проходив цей квест😥 \nРежим Чітера деактивовано", protect_content=True)
        return

    if user["is_passing"]:
        return

    bot.send_message(message.from_user.id,
                     '''
                     Привіт юний шукачу пригод і сьогодні на території Обінору я заховав для тебе скарб, який сам обожнюю від щирого серця. 
Зараз ти знаходишся на початку нашої подорожі у пошуках ельфійських скарбів.''')
    bot.send_sticker(message.from_user.id, "CAACANQQ", protect_content=True)
    keyboard = [
        [InlineKeyboardButton("Розпочати квест", callback_data="rules")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(message.from_user.id, "Готовий розпочати?",
                     reply_markup=reply_markup, protect_content=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith("rules"))
def category(query):
    user = db.get_user(query.message.chat.id)

    try:
        bot.delete_message(query.message.chat.id, query.message.id)
    except:
        pass
    if user["is_passed"]:  
        bot.send_message(query.message.chat.id, "Друже, ти вже проходив цей квест😥 \nРежим Чітера деактивовано")
        return
    bot.send_message(query.message.chat.id, '''Існує 5 різних шляхів до скарбу. Обирай свій та притримуйся тільки його. 
    Завдання квестого діалогу.''')

    bot.send_message(query.message.chat.id, '''
    Кожен відчайдуха заслуговує на свій приз і ти його теж відшукаєш. 
<b>Спочатку декілька правил:
    ''', parse_mode='html')

    db.set_user(query.message.chat.id, {"question_index": 0})

    user = db.get_user(query.message.chat.id)

    keyboard = [

        [InlineKeyboardButton("1. Переліт", callback_data="cat1")],
        [InlineKeyboardButton("2. Веселка", callback_data="cat2")],
        [InlineKeyboardButton("3. Мерехтіння ", callback_data="cat3")],
        [InlineKeyboardButton("4. Стежка ", callback_data="cat4")],
        [InlineKeyboardButton("5. Драконячі , callback_data="cat5")]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(query.message.chat.id, "Обери свій маршрут квесту:",
                     reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("cat"))
def category(query):
    user = db.get_user(query.message.chat.id)

    if user["is_passed"]:  
        bot.send_message(query.message.chat.id, "Друже, ти вже проходив цей квест😥 \nРежим Чітера деактивовано")
        return
    try:
        bot.delete_message(query.message.chat.id, query.message.id)
    except:
        pass
    bot.send_sticker(query.message.chat.id,
                     'CAACAgIAANQQ')
    if query.data == "cat1":
        index_of_category = 0
        bot.send_message(query.message.chat.id,
                         '''
<b>Підказка, де шукати першу легенду:</b
\nШукай наступну підказку у місці збору тролів…</i>
                         ''', parse_mode='html')
    elif query.data == "cat2":
        bot.send_message(query.message.chat.id,
                         '''
<b>Підказка, де шукати першу легенду:</b>
загадують бажання.</i>
                         ''', parse_mode='html')
        index_of_category = 1
    elif query.data == "cat3":
        bot.send_message(query.message.chat.id, '''
инає.
\nШукай наступну підказку у місці де ти здіймаєшся вище будиночків.</i>
''', parse_mode='html')
        index_of_category = 2
    elif query.data == "cat4":
        bot.send_message(query.message.chat.id, '''
    <b>Підказка, де шукати першу легенду:</b>
и ходив
\nШукай кюар код там, де грибами можна полікувати усе на світі.</i>
    ''', parse_mode='html')
        index_of_category = 3
    elif query.data == "cat5":
        bot.send_message(query.message.chat.id, '''
    <b>Підказка, де шукати першу легенду:</b
    ''', parse_mode='html')
        index_of_category = 4

    db.set_user(query.message.chat.id, {"question_index": 0, "category": index_of_category, "is_passing": True})
    user["question_index"] = 0
    user["category"] = index_of_category

    keyboard = [
        [InlineKeyboardButton("Запитання", callback_data="first")], ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(query.message.chat.id, "🙌Знайшов легенду, ознайомився з нею і готовий відповідати на запитання❓❓❓",
                     reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("first"))
def first_question(query):
    user = db.get_user(query.message.chat.id)

    if user["is_passed"]:  
        bot.send_message(query.message.chat.id, "Друже, ти вже проходив цей квест😥 \nРежим Чітера деактивовано")
        return
    try:
        bot.delete_message(query.message.chat.id, query.message.id - 1)
        bot.delete_message(query.message.chat.id, query.message.id)
    except:
        pass

    post = get_question_message(user)
    # print(post)
    if post is not None:
        bot.send_message(query.message.chat.id, post["text"],
                         reply_markup=post["keyboard"])


@bot.message_handler(commands=["stat"])
def statistic(message):
    if message.from_user.id == 'id1' or message.from_user.id == 'id2':
        all_count = db.users_count()
        all_vata_count = db.vata_count()
        day_count = db.day_users_count()
        day_vata_count = db.day_vata_count()
        bot.send_message(message.from_user.id, f"<b>Юзерів в базі за день: {day_count}"
                                               f"\nЗ них Отримали приз: {day_vata_count} </b>"
                                               f"\n\n<b>Всього Юзерів в базі: {all_count}"
                                               f"\nОтримали приз: {all_vata_count} </b>"
                                                                 , parse_mode='html')




@bot.callback_query_handler(func=lambda query: query.data.startswith("?ans"))
def answered(query):
    user = db.get_user(query.message.chat.id)

    if user["is_passed"] or not user["is_passing"]:
        return

    user["answers"].append(int(query.data.split("&")[1]))
    db.set_user(query.message.chat.id, {"answers": user["answers"]})

    post = get_answered_message(user)
    if user['question_index'] < 8:
        bot.edit_message_text(post['text_tips'], query.message.chat.id, query.message.id, parse_mode='html')

    if post is not None:
        bot.send_message(query.message.chat.id, post["text"],
                         reply_markup=post["keyboard"], parse_mode='html', protect_content=True)


@bot.callback_query_handler(func=lambda query: query.data == "?next")
def next(query):
    user = db.get_user(query.message.chat.id)
    try:
        bot.delete_message(query.message.chat.id, query.message.id - 1)
    except:
        pass


    user["question_index"] += 1
    db.set_user(query.message.chat.id, {"question_index": user["question_index"]})

    post = get_question_message(user)
    if post['sticker'] is not None:
        bot.send_sticker(query.message.chat.id, post['sticker'], protect_content=True)
    if post is not None:
        bot.edit_message_text(post["text"], query.message.chat.id, query.message.id,
                              reply_markup=post["keyboard"], parse_mode='html')


@bot.message_handler(content_types=["sticker"])
def repeat_all_messages(message):  
    file_info = message.sticker.file_id
    print(file_info)



def get_question_message(user):
    questions_count = db.questions_count(user['category'])
    if user["question_index"] == questions_count:
        count = 0
        for question_index, question in enumerate(db.questions.find({"category": user['category']})):
            if question["correct"] == user["answers"][question_index]:
                count += 1


        if count < 7:
            smile = (
                "😥 \nДруже, дуже шкода та в цей раз тобі не вдалося дати мінімум 7-8 правильних відповідей на запитання від Гедзьо Бурбеля. "
                "Але це не означає, що наступного разу не пощастить. Будь уважнішим і віримо в краще! ")
            sticker = '4XTUE'
        else:
            smile = ("😎 \nТи отримуєш такий бажаний подарунок - абонемент на какао та тістечко."
                     "\nПідходь у Цукерню та покажи їй цей переможний смайлик і вона тобі видасть твій подарунок. Гедзьо Бурбель тебе щиро вітає!")
            sticker = 'CAACAgIAAxkBAxk2BA'
            db.set_user(user["chat_id"], {"vata": True})

        text = f"Ти правильно відповів на {count} питань{smile}"
        db.set_user(user["chat_id"], {"is_passed": True, "is_passing": False})

        return {
            "text": text,
            "keyboard": None,
            "sticker": sticker,
        }

        question = db.get_question(user["question_index"], user["category"])


    if question is None:
        return

    keyboard = telebot.types.InlineKeyboardMarkup()
    for answer_index, answer in enumerate(question["answers"]):
        keyboard.row(telebot.types.InlineKeyboardButton(f"{chr(answer_index + 97)}) {answer}",
                                                        callback_data=f"?ans&{answer_index}"))

    text = f"Питання №{user['question_index'] + 1}\n\n{question['text']}"

    return {
        "text": text,
        "keyboard": keyboard,
        "sticker": None,
    }


def get_answered_message(user):
    question = db.get_question(user["question_index"], user["category"])
    tips = db.get_question(user["question_index"], user["category"])
    tips = tips["tips"]
    if user["question_index"] < 7:
        go_next = 'та закликає рухатися далі'
        text_button = (f"🙌Знайшов легенду, ознайомився з нею і готовий відповідати на запитання❓❓❓")
    else:
        go_next = ''
        text_button = ('Отримай свої результати!')
    text_tips = (
        f"Гедзьо Бурбель отримав відповідь на питання №{user['question_index'] + 1} ✅\n {go_next}😉\n\n <i>{tips}</i> ")

    keyboard = telebot.types.InlineKeyboardMarkup()
    if user["question_index"] == 7:
        button_text = 'Закінчити квест'
    else:
        button_text = 'Запитання'
    keyboard.row(telebot.types.InlineKeyboardButton(button_text, callback_data="?next"))

    return {
        "text": text_button,
        "text_tips": text_tips,
        "keyboard": keyboard
    }


bot.polling()
