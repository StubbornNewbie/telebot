import requests
import dbworker
import pickle
import markups as markup

import telebot
from config import token  # из файла config.py забираем нашу переменную с токеном

bot = telebot.TeleBot(token)



my_dict = {"Овен": 1,
           "Телец": 2,
           "Близнецы": 3,
           "Рак": 4,
           "Лев": 5,
           "Дева": 6,
           "Весы": 7,
           "Скорпион": 8,
           "Стрелец": 9,
           "Козерог": 10,
           "Водолей": 11,
           "Рыбы": 12,
           }


@bot.message_handler(commands=["start"])
def start(message):
    result = dbworker.check_user_exist(message.chat.id)
    if result is True:
        msg = """Привет! Прежде чем мы начнем, я хотел бы, чтобы вы выбрали свой знак зодиака. Нажмите на кнопки ниже, чтобы выбрать свой знак зодиака!\n\nЯ..."""
        bot.send_message(message.chat.id, text=msg, reply_markup=markup.initialization())


def initialization_complete(message, horoscope):
    msg = """Привет {}. Ты можешь /subscribe подписаться на наши обновления, или /unsubscribe отказаться от подписки, если вы больше не хотите получать никаких уведомлений.\n\nДаже если вы отказались от подписки, вы все равно можете использовать наши команды. Нажмите /help , чтобы увидеть больше."""
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id,
                          text=msg.format(horoscope))


@bot.message_handler(commands=["help"])
def cmd_help(message):
    msg = """*Available commands*\n\n/today - гороскоп на сегодня.\n/tomorrow - временно недоступно\n/settings - выбрать другой знак Задиака\n/subscribe - подписаться на рассылку\n/unsubscribe - отписаться"""
    bot.send_message(message.chat.id, parse_mode="Markdown", text=msg)


@bot.message_handler(commands=["today"])
def web_scrap_today(message):
    try:
        horoscope = dbworker.get_horoscope(message.chat.id)
        sign = my_dict[horoscope]
        url = "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={}".format(sign)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        data = soup.find_all("main", class_="main-horoscope")[0]
        date = data.p.strong.text
        todays_horoscope = data.p.strong.next_sibling.replace("-", "")
        bot.send_message(message.chat.id, text=date + " - " + horoscope + "\n\n" + todays_horoscope)
    except:
        bot.send_message(message.chat.id, text="не могу получить гороскоп на сегодня... 😭😭")


@bot.message_handler(commands=["tomorrow"])
def web_scrap_tomorrow(message):
    bot.send_message(message.chat.id, text="Эта команда не доступна.")


@bot.message_handler(commands=["subscribe"])
def subscribe(message):
    messageobj = pickle.dumps(message, pickle.HIGHEST_PROTOCOL)
    dbworker.add_to_subscribers(message.chat.id, messageobj)
    bot.send_message(message.chat.id, text="Здорово! вы подписались на нашу ежедневную рассылку.")


@bot.message_handler(commands=["unsubscribe"])
def unsubscribe(message):
    dbworker.remove_subscriber(message.chat.id)
    bot.send_message(message.chat.id, text="Прощай 😭😭... Вы отписались от нашей ежедневной рассылки.")


@bot.message_handler(commands=["settings"])
def settings(message):
    bot.send_message(message.chat.id, text="Что ты хочешь сделать?", reply_markup=markup.settings_menu())


def settings_change_horoscope(message):
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id,
                          text="Выбери свой гороскоп ещё раз",
                          reply_markup=markup.change_horoscope())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("horoscope_"):
        horoscope = call.data.split("_")[1]
        horoscope = horoscope.split(" ")[0]
        bot.answer_callback_query(call.id, text="Оу, ты " + horoscope + "!", show_alert=True)
        dbworker.initialize_user(call.message.chat.id, horoscope)
        initialization_complete(call.message, horoscope)
    elif call.data == "change_horoscope":
        bot.answer_callback_query(call.id)
        settings_change_horoscope(call.message)
    elif call.data.startswith("change_"):
        bot.answer_callback_query(call.id)
        horoscope = call.data.split("_")[1]
        horoscope = horoscope.split(" ")[0]
        dbworker.change_db_horoscope(call.message.chat.id, horoscope)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Знак Зодиака выбран! Нажми /today , чтобы посмотреть 😄",
                              reply_markup=markup.horoscope_done_troll(horoscope))
    elif call.data == "о-о":
        bot.answer_callback_query(call.id, text="о-о")


if __name__ == '__main__':
    bot.polling(none_stop=True)
