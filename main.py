
import mysql.connector #database
import telebot
from telebot import types


API_TOKEN = '6443601430:AAFsYzeESGE77uJHGhd931QGvPfvunWzsCY'
bot = telebot.TeleBot(API_TOKEN)
text1 = "Стоимость билета: 3500р\n\nВАЖНО: При покупке билета обязательно указывай ФИО в сообщении к переводу.\n\nТИНЬКОФФ:\n2200 7004 3633 8304\n\nСБЕР:\n5469 9804 7066 3226\n\nПо номеру телефона:\n+7 (999) 560-50-04\nМаксим Викторович Е.\n\nПОСЛЕ СОВЕРШЕНИЯ ОПЛАТЫ:\n\nПожалуйста, напиши свое ФИО"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    oplata = types.InlineKeyboardButton(text="Оплатить", callback_data="oplata")
    markup.add(oplata)
    bot.send_message(message.chat.id,
                     text=f"Добро пожаловать в игру, {message.from_user.first_name}!\n\nДля регистрации в качестве игрока тебе необходимо внести кассовый сбор.\n\nНажми «Оплатить» для продолжения регистрации.".format(
                         message.from_user), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "oplata":
        msg = bot.send_message(call.message.chat.id, text1)
        bot.register_next_step_handler(msg, get_data)

def get_data(message):
    global data
    data = message.text
    bot.send_message(message.from_user.id, 'А теперь напиши номер группы')
    bot.register_next_step_handler(message, get_group)

def get_group(message):
    global group
    group = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text='Спасибо! А теперь проверь, всё ли введено верно: Ты - ' + data + ' из группы ' + group + '?' ' Нажми «да», если все верно, и «нет» - если нужно перезаписать данные', reply_markup=markup)


@bot.message_handler(content_types=['text', 'url'])
def func(message):
    global data
    connection = mysql.connector.connect(
        host="romanloqi.mysql.pythonanywhere-services.com",
        user="romanloqi",
        password="e2F@NbJx.r4rTg.",
        database="romanloqi$default",
    )
    cursor = connection.cursor() #database

    if (message.text == "Да"):
        data_list=data.split()
        cursor.execute("INSERT INTO guests(фамилия, имя, отчество, группа, оплата) VALUES(%s, %s, %s, %s, %s)", (data_list[0], data_list[1], data_list[2], group, "Да")) #database
        connection.commit() #database
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button = types.InlineKeyboardButton(text = 'Ссылка на форму', url ='https://docs.google.com/forms/d/e/1FAIpQLSdxTMnzs1w8tbf4Qixem0e1Fpsc2yfCt_6ZnTLXgjfcI2-ZMw/viewform')
        keyboard.add(button)
        bot.send_message(message.chat.id, 'Отлично! Ожидай подтверждения оплаты от администратора.\n\nА пока ожидаешь - заполни форму по ссылке внизу.', reply_markup=keyboard)
    elif (message.text == "Нет"):
        not_okey = bot.send_message(message.chat.id, 'Введи свое ФИО заново')
        bot.register_next_step_handler(not_okey, get_data)
        data_list=data.split()
        cursor.execute("INSERT INTO guests(фамилия, имя, отчество, группа, оплата) VALUES(%s, %s, %s, %s, %s)", (data_list[0], data_list[1], data_list[2], group, "Да")) #database
        connection.commit() #database
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button = types.InlineKeyboardButton(text = 'Ссылка на форму', url ='https://docs.google.com/forms/d/e/1FAIpQLSdxTMnzs1w8tbf4Qixem0e1Fpsc2yfCt_6ZnTLXgjfcI2-ZMw/viewform')
        keyboard.add(button)
        bot.send_message(message.chat.id, 'Отлично! Ожидай подтверждения оплаты от администратора.\n\nА пока ожидаешь - заполни форму по ссылке внизу.', reply_markup=keyboard)




bot.polling(none_stop=True)
