import telebot
from telebot import types

TOKEN = ''  # Замініть на свій токен

questions = [
    {
        "question": "Яка хімічна речовина позначається символом H2O?",
        "options": ["Кисень", "Водень", "Азот", "Вода"],
        "correct": 3
    },
    {
        "question": "Який художник написав картину 'Мона Ліза'?",
        "options": ["Пабло Пікассо", "Леонардо да Вінчі", "Вінсент Ван Гог", "Рафаель"],
        "correct": 1
    },
    {
        "question": "Яку планету вважають найбільшою в Сонячній системі?",
        "options": ["Венера", "Земля", "Юпітер", "Марс"],
        "correct": 2
    },
    {
        "question": "Канадський Коннор МакДевід - висхідна зірка в якому виді спорту?",
        "options": ["Хокей", "Футбол", "Теніс", "Плавання"],
        "correct": 1
    },
    {
        "question": "Якби Земля була перетворена на чорну діру, яким був би діаметр її горизонту подій?",
        "options": ["1М", "50см", "20мм", "1мм"],
        "correct": 3
    },
]

bot = telebot.TeleBot(TOKEN)

user_scores = {}


@bot.message_handler(commands=['start'])
def start(message):
    """
    Обробник команди /start.

    Запускає тест для користувача.
    """

    user_id = message.chat.id
    user_scores[user_id] = {"score": 0, "current_question": 0}
    send_question(user_id)


def send_question(user_id):
    """
    Відправляє користувачу наступне запитання.

    Якщо користувач досягнув останнього запитання, то тест завершується.
    """

    user_data = user_scores[user_id]
    current_question = user_data["current_question"]

    if current_question < len(questions):
        question_data = questions[current_question]
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        options = question_data["options"]
        for option in options:
            markup.add(types.KeyboardButton(option))

        bot.send_message(user_id, question_data["question"], reply_markup=markup)
    else:
        bot.send_message(user_id, f"Тест завершено! Ваш рахунок: {user_scores[user_id]['score']}",
                         reply_markup=types.ReplyKeyboardRemove())
        del user_scores[user_id]


@bot.message_handler(func=lambda message: True)
def check_answer(message):
    """
    Перевіряє правильність відповіді користувача.

    Якщо відповідь правильна, то користувач отримує бал.
    """

    user_id = message.chat.id
    if user_id in user_scores:
        user_data = user_scores[user_id]
        current_question = user_data["current_question"]
        question_data = questions[current_question]
        correct_option = question_data["correct"]

        if message.text == question_data["options"][correct_option - 1]:
            user_scores[user_id]["score"] += 1

        user_scores[user_id]["current_question"] += 1
        send_question(user_id)


bot.polling(none_stop=True)
