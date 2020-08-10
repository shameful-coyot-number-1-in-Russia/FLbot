import telebot
from bs4 import BeautifulSoup as BS
import requests
bot = telebot.TeleBot('1393195284:AAEaNNJ1w2BiG6SdmtSVU1qzc9JurjN87cI')

oldid=0
tf=0

@bot.message_handler(commands=['start'] or ['help'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Включить', 'Выключить')
    keyboard.row('Поддержать автора денюжкой ;3')
    bot.send_message(message.chat.id, 'Кнопки включены', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global tf
    if message.text == "Поддержать автора денюжкой ;3":
        bot.send_message(message.from_user.id, "QIWI: PZRNQT1VRSS\nКарта: 4693 9575 5861 3282")
    if message.text == "Выключить":
        bot.send_message(message.chat.id, "Оповещение о заказах выключено")
        tf = 0
    if message.text == "Включить":
        bot.send_message(message.from_user.id, "Оповещение о заказах включено")
        tf = 1
        global oldid
        while (1):
            if tf:
                pages = []
                ans = ""
                pages.append(requests.get('https://www.fl.ru/projects'))
                for r in pages:
                    html = BS(r.content, 'html.parser')
                    for i in html.select(".b-post"):
                        if "b-post__pin" in str(i.select(".b-post__pin")):
                            print(i.select(".b-post__pin"))
                        else:
                            id = list(map(str, list(map(str, str(i).split('id="')))[1].split('">')))[0]
                            name = \
                            list(map(str, list(map(str, str(i.select(".b-post__link")).split('>')))[1].split('<')))[0]
                            title = list(map(str, list(map(str, str(i).split('<div class="b-post__txt "> ')))[1].split(
                                '</div>')))[
                                0]
                            mon = list(map(str, list(map(str, str(i).split('&nbsp;')))[0].split('>')))[-1]
                            url = "fl.ru" + \
                                  list(map(str,
                                           list(map(str, str(i).split('class="b-post__link" href="')))[1].split('"')))[
                                      0]
                            if list(map(str, str(i).split('&nbsp;')))[1][0] == '₽':
                                mon += "₽"
                            else:
                                mon += "$"
                            ans += name + "   " + mon + "   " + url + "   " + "\n" + title
                            if id != oldid:
                                try:
                                    bot.send_message(message.chat.id, ans)
                                except:
                                    print("Чет не так, но ок")
                                    break
                            oldid = id
                            ans = ""
                            break

bot.polling()