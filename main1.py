import time

import telebot
from pymongo import MongoClient
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("6666846921:AAGJU9TIBKHBlRfK2uCijCKvRH1tSCsqWVg")


class DataBase:
    def __init__(self):
        cluster = MongoClient(
            "mongodb+srv://gedzio:YjnM5vHkkE4SUk4Y@cluster0.yuqwjae.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.db = cluster["QuizBot"]
        self.users = self.db["Users"]
        self.questions = self.db["Questions"]
        self.questions_count = len(list(self.questions.find({})))

    def get_user(self, chat_id):
        user = self.users.find_one({"chat_id": chat_id})

        if user is not None:
            return user

        user = {
            "chat_id": chat_id,
            "is_passing": False,
            "is_passed": False,
            "question_index": None,
            "category": None,
            "answers": []
        }
        print(user)

        self.users.insert_one(user)

        return user

    def set_user(self, chat_id, update):
        self.users.update_one({"chat_id": chat_id}, {"$set": update})

    def get_question(self, index,category):
        print('ind',index, category)
        return self.questions.find_one({"question": index, "category": category})

    #def get_tips(self, index):
        #return self.


db = DataBase()


@bot.message_handler(commands=["start"])
def start(message):
    user = db.get_user(message.chat.id)
    print(user)
   #checking of second activity
   # if user["is_passed"]:
       # bot.send_message(message.from_user.id, "Друже, ти вже проходив цей квест😥 \nРежим Чітера деактивовано")
       # return

    # if user["is_passing"]:
    #	return

    bot.send_message(message.from_user.id,
                     '''
                     Привіт юний шукачу пригод, мене звати Гедзьо Бурбель і сьогодні на території Обінору я заховав для тебе скарб, який сам обожнюю від щирого серця. 
Зараз ти знаходишся на початку нашої подорожі у пошуках ельфійських скарбів.''')
    # bot.send_photo(message.from_user.id, "https://cdn.pixabay.com/photo/2024/05/05/11/47/nature-8741046_960_720.jpg")
    bot.send_sticker(message.from_user.id,"CAACAgIAAxkBAAIE9WbArtJNuJffgO6fxkJjEbCGvZyzAALnWAACh9PRScaRmqGg_zL5NQQ")
    keyboard = [

            [InlineKeyboardButton("Розпочати квест", callback_data="rules")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(message.from_user.id, "Готовий розпочати?",
                     reply_markup=reply_markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("rules"))
def category(query):
    user = db.get_user(query.message.chat.id)
    bot.send_message(query.message.chat.id, '''Існує 5 різних шляхів до скарбу. Обирай свій та притримуйся тільки його. 
    Завдання квесту – це дати 8 правильних відповідей на запитання з Telegram-боту.
    ❗️Відповіді на ці запитання можна знайти у засекречених легендах📜, які заховані за кюар кодами. 
    А відповідно кюар коди потрібно шукати за підказками з нашого діалогу.''')


    bot.send_message(query.message.chat.id, '''
    Кожен відчайдуха заслуговує на свій приз і ти його теж відшукаєш. 
<b>Спочатку декілька правил:
1. Уважно читай увесь текст.
2. Цей квест треба проходити по-одному учаснику. По-принципу «один учасник – один переможець».
3. Будь обережним та не порушуй правил поведінки на території парку. </b> 
                         
    ''', parse_mode='html')

    db.set_user(query.message.chat.id, {"question_index": 0})

    user = db.get_user(query.message.chat.id)

    keyboard = [

            [InlineKeyboardButton("1. Переліт Жабокрила", callback_data="cat1")],
            [InlineKeyboardButton("2. Веселка тролів", callback_data="cat2")],
        [InlineKeyboardButton("3. Мерехтіння ельфів", callback_data="cat3")],
            [InlineKeyboardButton("4. Стежка Грибмедя", callback_data="cat4")],
            [InlineKeyboardButton("5. Драконячі пагорби", callback_data="cat5")]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(query.message.chat.id, "Обери свій маршрут квесту:",
                     reply_markup=reply_markup)


# post = get_category(user)
# if post is not None:
# bot.send_message(message.from_user.id, post["text"], reply_markup=post["keyboard"])




@bot.callback_query_handler(func=lambda call:call.data.startswith("cat"))
def category(query):
    user = db.get_user(query.message.chat.id)
    if query.data == "cat1":
        index_of_category = 0
        bot.send_sticker(query.message.chat.id, 'CAACAgIAAxkBAAIFJWbAskH-Swer80QDoYuHQLVpJ8NGAAKJVAAClgbRSUUqrGoj-GKJNQQ')
        bot.send_message(query.message.chat.id,
                         '''
<b>Підказка, де шукати першу легенду:</b>
\n<i>Біля ватри тролі зібрались вночі, 
Легенди старі розповідали вони.
Вогонь танцює в їхніх очах,
Звук їхніх слів лунав у горах.
Шукай наступну підказку у місці збору тролів…</i>
                         ''', parse_mode='html')
    elif query.data == "cat2":
        index_of_category = 1
    elif query.data == "cat3":
        index_of_category = 2
    db.set_user(query.message.chat.id, {"question_index": 0, "category":index_of_category, "is_passing": True})
    user["question_index"] = 0
    user["category"] = index_of_category

    keyboard = [

            [InlineKeyboardButton("Запитання", callback_data="first")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(query.message.chat.id, "🙌Знайшов легенду, ознайомився з нею і готовий відповідати на запитання❓❓❓",
                     reply_markup=reply_markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("first"))
def first_question(query):
    user = db.get_user(query.message.chat.id)
    post = get_question_message(user)
    print(post)
    if post is not None:
        bot.send_message(query.message.chat.id, post["text"],
                              reply_markup=post["keyboard"])


@bot.callback_query_handler(func=lambda query: query.data.startswith("?ans"))
def answered(query):
    user = db.get_user(query.message.chat.id)

    if user["is_passed"] or not user["is_passing"]:
        return

    user["answers"].append(int(query.data.split("&")[1]))
    db.set_user(query.message.chat.id, {"answers": user["answers"]})


    post = get_answered_message(user)
    bot.edit_message_text( post['text_tips'],query.message.chat.id,query.message.id, parse_mode='html')

    if post is not None:
        bot.send_message( query.message.chat.id, post["text"],
                              reply_markup=post["keyboard"], parse_mode='html')


@bot.callback_query_handler(func=lambda query: query.data == "?next")
def next(query):
    user = db.get_user(query.message.chat.id)

    if user["is_passed"] or not user["is_passing"]:
        return

    user["question_index"] += 1
    print(user["question_index"])
    db.set_user(query.message.chat.id, {"question_index": user["question_index"]})



    post = get_question_message(user)
    print(post)
    if post['sticker'] is not None:
        bot.send_sticker()
    if post is not None:
        bot.edit_message_text(post["text"], query.message.chat.id, query.message.id,
                              reply_markup=post["keyboard"], parse_mode='html')



@bot.message_handler(content_types=["sticker"])
def repeat_all_messages(message): # Название функции не играет никакой роли
    file_info = message.sticker.file_id
    print(file_info)


def get_question_message(user):
    if user["question_index"] == db.questions_count:
        count = 0
        for question_index, question in enumerate(db.questions.find({})):
            print("qu in, ques:",question_index, question)
            print(user["answers"][question_index])
            if question["correct"] == user["answers"][question_index]:
                count += 1
                print(user["answers"][question_index])
        all_marks = db.questions_count

        if count < all_marks - 1:
            smile = ("😥 \nДруже, дуже шкода та в цей раз тобі не вдалося дати мінімум вісім правильних відповідей на запитання від Гедзьо Бурбеля. "
                     "Але це не означає, що наступного разу не пощастить. Будь уважнішим і віримо в краще! ")
            sticker ='CAACAgIAAxkBAAIE52a7N5OlnGhGy0jEbnMAASjbG3HGBwAC51gAAofT0UnGkZqhoP8y-TUE'
        else:
            smile = ("😎 \nТи отримуєш такий бажаний подарунок – абонемент на безкоштовну цукрову вату. "
                     "Підходь до ельфійки, яка робить її поруч з Цукернею та покажи їх цей переможний смайлик. Гедзьо Бурбель тебе щиро вітає!")

        text = f"Ти правильно відповів на {count} питань{smile}"

        db.set_user(user["chat_id"], {"is_passed": True, "is_passing": False})

        return {
            "text": text,
            "keyboard": None,
            "sticker": sticker,
        }

    print('user:',user)
    print('user category:',user["category"])
    print('user index:',user["question_index"])
    question = db.get_question(user["question_index"],user["category"])
    print(question)

    if question is None:
        return

    keyboard = telebot.types.InlineKeyboardMarkup()
    for answer_index, answer in enumerate(question["answers"]):
        keyboard.row(telebot.types.InlineKeyboardButton(f"{chr(answer_index + 97)}) {answer}",
                                                        callback_data=f"?ans&{answer_index}"))

    text = f"Питання №{user['question_index']+1}\n\n{question['text']}"


    return {
        "text": text,
        "keyboard": keyboard,
        "sticker": None,
    }


def get_answered_message(user):
    question = db.get_question(user["question_index"],user["category"])
    print(question)
    tips = db.get_question(user["question_index"],user["category"])
    tips = tips["tips"]
    text_tips = (f"Гедзьо Бурбель отримав відповідь на питання №{user['question_index']+1} ✅\nта закликає рухатися далі😉\n\n <i>{tips}</i> ")



    text_button = (f"🙌Знайшов легенду, ознайомився з нею і готовий відповідати на запитання❓❓❓")

    keyboard = telebot.types.InlineKeyboardMarkup()
    if user["question_index"] == db.questions_count-1:
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
