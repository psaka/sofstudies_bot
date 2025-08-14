import telebot
from telebot import types
import os

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))  # Токен теперь берётся из переменных окружения

# Обработка команд
@bot.message_handler(commands=['text', 'text2'])
def send_text(message):
    bot.send_message(message.chat.id, 'Текст с <b>HTML</b> <em><u>форматированием</u></em>', parse_mode='html')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Она не работает..', callback_data='nune'))
    markup.add(types.InlineKeyboardButton('И она тоже', callback_data='nune'))
    bot.send_message(message.chat.id, f'🦉 Здравствуй, {message.from_user.first_name}! Я Сова Афина, и я здесь, чтобы твоя подготовка к ЕГЭ по обществу была легче и понятнее. 😊

Не стесняйся обращаться! Я помогу тебе:

✅ Решить тесты – отрабатывай задания в формате ЕГЭ каждый день
✅ Получить материалы – выбирай тему и получай структурированные конспекты ✏️  
✅ Найти определение – Забыл термин? Спроси – и я тут же подскажу точную формулировку! 📖

👇 Я тут чтобы упростить твой путь к высоким баллам. Выбирай пункт ниже и поехали!', reply_markup=markup)

@bot.message_handler(commands=['send'])
def send_options(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Отправить картинку', callback_data='send_1'))
    markup.add(types.InlineKeyboardButton('Отправить PDF', callback_data='send_2'))
    bot.send_message(message.chat.id, 'Выбери, что отправить:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'send_1':
        try:
            with open('fox_pic.jpg', 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo)
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, 'а вот и нет файла')
    elif call.data == 'send_2':
        try:
            with open('fox_doc.pdf', 'rb') as doc:
                bot.send_document(call.message.chat.id, doc)
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, 'а вот и нет файла')
    bot.answer_callback_query(call.id)

# Обработка текста
@bot.message_handler()
def reply_to_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    elif message.text.lower() == 'пока':
        bot.reply_to(message, f'Пока, {message.from_user.first_name}!')

if __name__ == '__main__':
    bot.polling(non_stop=True)
