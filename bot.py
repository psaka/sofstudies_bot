import telebot
from telebot import types
import os
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))  # Токен теперь берётся из переменных окружения
CHANNEL_ID = '@sofstudies'

@bot.message_handler(commands=['menu'])
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Конспекты", "Топ-20 планов", "Решать тесты")
    bot.send_message(message.chat.id, "Главное меню! Выбирай пункт ниже и поехали!", reply_markup=markup)

# функция, проверяющая подписку 
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False

# start
@bot.message_handler(commands=['start'])
def start(message):
        global welcome_text_subcribed
        global welcome_text_unsubcribed
        welcome_text_subcribed = (
            f"🦉 Здравствуй, {message.from_user.first_name}! Я Сова Афина, и я здесь, чтобы твоя подготовка к ЕГЭ по обществу была легче и понятнее. 😊\n\n"
            "Не стесняйся обращаться! Я помогу тебе:\n\n"
            "✅ Решить тесты – отрабатывай задания в формате ЕГЭ каждый день\n"
            "✅ Получить материалы – выбирай тему и получай структурированные конспекты ✏️\n"  
            "✅ Найти определение – Забыл термин? Спроси – и я тут же подскажу точную формулировку! 📖\n\n"
            "👇 Я тут чтобы упростить твой путь к высоким баллам."
        )
        welcome_text_unsubcribed = (
            f"🦉 Здравствуй, {message.from_user.first_name}! Я Сова Афина, и я здесь, чтобы твоя подготовка к ЕГЭ по обществу была легче и понятнее. 😊\n\n"
            "Не стесняйся обращаться! Я помогу тебе:\n\n"
            "✅ Решить тесты – отрабатывай задания в формате ЕГЭ каждый день\n"
            "✅ Получить материалы – выбирай тему и получай структурированные конспекты ✏️\n"  
            "✅ Найти определение – Забыл термин? Спроси – и я тут же подскажу точную формулировку! 📖\n\n"
            "👇 Я тут чтобы упростить твой путь к высоким баллам. Подпишись на канал, чтобы получить доступ к моей базе знаний!"
        )
        if check_subscription(message.from_user.id):
            bot.send_message(message.chat.id, welcome_text_subcribed)
            show_main_menu(message.chat.id)
        else:
            show_subscription_request(message.chat.id)

# Показ требования подписки
def show_subscription_request(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Подписаться на канал!', callback_data='nune', url=f"https://t.me/{CHANNEL_ID[1:]}"))
    markup.add(types.InlineKeyboardButton("Я уже подписан/а!", callback_data="check_subscription"))
    
    bot.send_message(chat_id, 
                    welcome_text_unsubcribed,
                    reply_markup=markup)

# Обработчик кнопки проверки подписки
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_sub(call):
    if check_subscription(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "Ты пока не подписан/а", show_alert=True)


# Главное меню 
def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Конспекты", "Топ-20 планов", "Решать тесты")
    bot.send_message(chat_id, "Главное меню! Выбирай пункт ниже и поехали!", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Решать тесты")
def tests_start_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("тест 1", "тут пусто", "пусто..")
    bot.send_message(message.chat.id, "Какой тест будем решать?", reply_markup=markup)



# ТЕСТ 1 
test_1_questions = [
    {
        'question': '''Выберите верные суждения об особенностях социального познания, отличающих его от иных видов познания, и запишите цифры, под которыми они указаны, в порядке возрастания.

1) К особенностям социального познания относится использование научных методов.
2) Социальное познание основывается на информации, собранной учеными.
3) Осуществляющий социальное познание субъект включен в объект познания.
4) Социальное познание осуществляется на основе точных наук.
5) В социальном познании мнение и интересы исследователя влияют на объяснение и интерпретацию фактов.''',
        'answer': '35'
    },
    {
        'question': '''Выберите верные суждения о международной торговле и запишите в порядке возрастания цифры, под которыми они указаны.

1) Отказ от международной торговли обязательно приводит к повышению качества производимых товаров и услуг и росту их конкурентоспособности.
2) Внешнеторговая политика, ориентированная на свободный обмен товарами, называется протекционизмом.
3) Тарифные и нетарифные барьеры нацелены на стимулирование роста ВВП и защиту отечественных производителей от конкуренции.
4) К нетарифным барьерам относится введение квот на импорт товаров.
5) Импортные пошлины направлены на повышение предложения товаров, производимых за рубежом. ''',
        'answer': '34'
    },
    {
        'question': '''Выберите верные суждения о предпринимательской деятельности и ее организационно-правовых
формах и запишите цифры, под которыми они указаны.

1) Предпринимательство — это инициативная самостоятельная деятельность граждан и их объединений, соответствующая закону и направленная на получение прибыли.
2) Гражданин вправе заниматься предпринимательской деятельностью без образования юридического лица.
3) Публичное акционерное общество размещает акции и ценные бумаги для обращения путем открытой подписки.
4) К унитарным юридическим лицам относятся производственные кооперативы и акционерные общества.
5) Жилищные, гаражные, дачные кооперативы осуществляют предпринимательскую деятельность и являются коммерческими организациями. ''',
        'answer': '123'
    }
]

# Глобальные 
user_scores = {}
current_question = {}

@bot.message_handler(func=lambda msg: msg.text == "тест 1")
def start_test_1(message):
    user_id = message.from_user.id
    user_scores[user_id] = 0  # запускаем счетчик очков
    current_question[user_id] = 0  # Начинаем с первого вопроса
    
    #  первый вопрос
    bot.send_message(message.chat.id, f"Вопрос 1:\n{test_1_questions[0]['question']}")
    bot.register_next_step_handler(message, check_test_1_answer)

def check_test_1_answer(message):
    user_id = message.from_user.id
    question_index = current_question[user_id]
    correct_answer = test_1_questions[question_index]['answer']
    
    if message.text.strip() == correct_answer:
        user_scores[user_id] += 1  
        bot.send_message(message.chat.id, "Правильно!")
    else:
        bot.send_message(message.chat.id, f"Неправильно! Правильный ответ: {correct_answer}")
    
    # к следующему вопросу или завершаем тест
    current_question[user_id] += 1
    
    if current_question[user_id] < len(test_1_questions):
        # следующий вопрос
        next_question = test_1_questions[current_question[user_id]]
        bot.send_message(message.chat.id, f"Вопрос {current_question[user_id]+1}:\n{next_question['question']}")
        bot.register_next_step_handler(message, check_test_1_answer)
    else:
        # Тест завершен, результаты
        total = len(test_1_questions)
        score = user_scores[user_id]
        bot.send_message(message.chat.id, f"Умничка, ты прошел тест!!\nТы набрал/а {score} из {total} баллов")
        
        # Очищаем состояние пользователя
        del user_scores[user_id]
        del current_question[user_id]
        
        show_main_menu(message.chat.id)  # Возвращаем в меню





# привет, пока, секретная информация для своих. общалка-развлекаловка текстом, не команды 
@bot.message_handler()
def reply_to_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    elif message.text.lower() == 'пока':
        bot.reply_to(message, f'Пока, {message.from_user.first_name}!')
    elif message.text.lower() == 'мяу':
        bot.send_message(message.chat.id, f'мяу  :3')
    elif message.text.lower() == '1234':
        bot.send_message(message.chat.id, f'супер секретная информация для своих')

# Проверка подписки перед обработкой любых сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if not check_subscription(message.from_user.id):
        show_subscription_request(message.chat.id)
    else:
        # Обработка обычных команд
        pass

if __name__ == '__main__':
    bot.polling(non_stop=True)
