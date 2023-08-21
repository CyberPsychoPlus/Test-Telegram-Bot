import telebot
from telebot import types

TOKEN = ''  # Замените на свой токен

questions = [
    {
        "question": "Какое химическое вещество обозначается символом H2O?",
        "options": ["Кислород", "Водород", "Азот", "Вода"],
        "correct": 3
    },
    {
        "question": "Какой художник написал картину 'Мона Лиза'?",
        "options": ["Пабло Пикассо", "Леонардо да Винчи", "Винсент Ван Гог", "Рафаэль"],
        "correct": 1
    },
    {
        "question": "Какая планета считается самой большой в Солнечной системе?",
        "options": ["Венера", "Земля", "Юпитер", "Марс"],
        "correct": 2
    }
]

bot = telebot.TeleBot(TOKEN)

user_scores = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_scores[user_id] = {"score": 0, "current_question": 0}
    send_question(user_id)


def send_question(user_id):
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
        bot.send_message(user_id, f"Тест завершен! Ваш счет: {user_scores[user_id]['score']}",
                         reply_markup=types.ReplyKeyboardRemove())
        del user_scores[user_id]


@bot.message_handler(func=lambda message: True)
def check_answer(message):
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
