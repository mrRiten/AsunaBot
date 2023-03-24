import datetime
import threading
import requests
from bs4 import BeautifulSoup
import telebot as tl
from threading import Thread
import time
import json
import schedule as sch

# TelBotToken
bot = tl.TeleBot('Token')


def get_inf():

    # get URL
    Weather_URl = 'https://pogoda7.ru/prognoz/gorod943-Russia-Yaroslavskaya_oblast-Yaroslavl/1days/full'
    News_URL = 'https://news.mail.ru'
    EUR_RUB_URL = 'https://www.google.ru/search?q=курс+евро&newwindow=1&sxsrf=ALiCzsbmIKfsc07wLE9uI4bWbSIobDDIBw%3A1663183301779&source=hp&ei=xSkiY-X7K-iJrwTA0Ib4BA&iflsig=AJiK0e8AAAAAYyI31XS_1auoVsGnOhUq4cRcKIsjaDWN&oq=курс+евр&gs_lcp=Cgdnd3Mtd2l6EAEYADIJCCMQJxBGEIICMggIABCABBCxAzIICAAQgAQQsQMyCwgAEIAEELEDEIMBMggIABCABBCxAzIFCAAQgAQyCAgAEIAEELEDMggIABCABBCxAzIFCAAQgAQyBQgAEIAEOgcIIxDqAhAnOgQIIxAnOgsILhCxAxCDARDUAjoLCC4QgAQQxwEQrwE6CAguEIAEELEDOgsILhCABBCxAxCDAVC3AViROWDWQGgCcAB4AYABwwGIAZAGkgEDNy4ymAEAoAEBsAEK&sclient=gws-wiz'
    USD_RUB_URL = 'https://www.google.ru/search?q=курс+доллара&newwindow=1&sxsrf=ALiCzsZhuTfiBDkZ3oW2XvlDH5r1aE-r5Q%3A1662989007957&source=hp&ei=zzIfY7C5OOrJrgTrpYDICw&iflsig=AJiK0e8AAAAAYx9A37RprR8CGXkh12834Bi3o2qN2ErT&oq=курс+&gs_lcp=Cgdnd3Mtd2l6EAEYADIJCCMQJxBGEIICMgQIIxAnMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyBQgAEIAEMggIABCABBCxAzIFCAAQgAQyCAgAEIAEELEDMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwE6BwgjEOoCECc6CwguEIAEEMcBEK8BOggILhCxAxCDAToICAAQsQMQgwFQlw1YnRJglRloAXAAeAGAAcMBiAGjA5IBAzQuMZgBAKABAbABCg&sclient=gws-wiz'
    JPY_RUB_URL = 'https://www.google.ru/search?q=курс+йены&newwindow=1&sxsrf=AJOqlzWD96jS2WKtLBOeJ9hLg0aru6n39w%3A1677612906829&source=hp&ei=alf-Y7nxL-6krgTyzJOwBw&iflsig=AK50M_UAAAAAY_5leoYfJ1sMgHO-9JkTCM7yqAgVV6bP&oq=курс+ен&gs_lcp=Cgdnd3Mtd2l6EAMYATIFCAAQgAQyDQgAEIAEELEDEIMBEAoyDQgAEIAEELEDEIMBEAoyBwgAEIAEEAoyBwgAEIAEEAoyBwgAEIAEEAoyBwgAEIAEEAoyBwgAEIAEEAoyBwgAEIAEEAoyBwgAEIAEEAo6BwgjEOoCECc6DQguEMcBEK8BEOoCECc6BAgjECc6CwgAEIAEELEDEIMBOgsILhCABBCxAxCDAToICAAQsQMQgwE6CwguEIAEEMcBEK8BOg4ILhCvARDHARDUAhCABDoICAAQgAQQsQM6CggAEIAEELEDEApQtgtY_SVg5T5oAnAAeAGAAfgDiAHdCpIBBzYuNC0xLjGYAQCgAQGwAQo&sclient=gws-wiz'
    headers = {'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100 (Edition Yx GX)'}

    # parsing weather
    full_page_Weather = requests.get(Weather_URl, headers=headers)
    soup_Weather = BeautifulSoup(full_page_Weather.content, 'html.parser')
    weather_now = soup_Weather.findAll('div', {'class': 'grid precip'})

    # parsing USD from Google
    full_page_RUB_USD = requests.get(USD_RUB_URL, headers=headers)
    soupUSD_RUB = BeautifulSoup(full_page_RUB_USD.content, 'html.parser')
    ConvertUSD = soupUSD_RUB.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})

    # parsing EUR from Google
    full_page_RUB_EUR = requests.get(EUR_RUB_URL, headers=headers)
    soupEUR_RUB = BeautifulSoup(full_page_RUB_EUR.content, 'html.parser')
    ConvertEUR = soupEUR_RUB.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})

    # parsing JPY from Google
    full_page_RUB_JPY = requests.get(JPY_RUB_URL, headers=headers)
    soupJPY_RUB = BeautifulSoup(full_page_RUB_JPY.content, 'html.parser')
    ConvertJPY = soupJPY_RUB.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})

    # parsing news Mail.ru
    full_page_News = requests.get(News_URL, headers=headers)
    soup_News = BeautifulSoup(full_page_News.content, 'html.parser')
    news = soup_News.findAll('div', {'class': 'cols__wrapper', 'class': 'cols__column cols__column_small_percent-50 cols__column_medium_percent-33 cols__column_large_percent-33'})

    # assignment text from Mail.ru news
    news_output0 = news[0].text
    news_output1 = news[1].text
    news_output2 = news[2].text
    news_output3 = news[3].text
    news_output4 = news[4].text
    news_output5 = news[5].text

    inf = f'🗓Сегодня {datetime.datetime.now().strftime("%Y-%d-%m")}'\
        f'\n\nКурс Доллара: {ConvertUSD[0].text} рублей'\
        f'\n💶Курс Евро: {ConvertEUR[0].text} рублей'\
        f'\n💴Курс Йен: {ConvertJPY[0].text} рублей\n' \
          f'\n⛅Погода \n{weather_now[0].text}' \
          f'\n\n📰Новости:' \
          f'\n📌{news_output0}' \
          f'\n📌{news_output1}' \
          f'\n📌{news_output2}' \
          f'\n📌{news_output3}' \
          f'\n📌{news_output4}' \
          f'\n📌{news_output5}'

    print('Updated!')

    # writing loga to file
    with open('logs.txt', 'a') as file_obj:
        print(f'Updated at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', file=file_obj)
    file_obj.close()

    return inf


# Work bot code
# main inf
def main_inf():
    # open json
    with open('data.json', 'r') as file_obj:
        data_from_json = json.load(file_obj)
    # get user id for send message
    try:
        for user in data_from_json:
            name = data_from_json[f'{user}']['username']
            schedule_text = data_from_json[f'{user}']['schedule_text']
            bot.send_message(user, f'{name}, будте в курсе событий!\n\n{get_inf()}\n\n📑Ваше расписание:\n{schedule_text}')

            # write logs
            with open('logs.txt', 'a+') as logs_obj:
                print(f'{user} - bot send mes at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', file=logs_obj)
                logs_obj.close()
    except Exception as e:
        with open('logs.txt', 'a+') as logs_obj:
            print(f'{e} - {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', file=logs_obj)
            logs_obj.close()


# create new thread
def create_th(message):
    send_main_th = Thread(target=main_mes, args=[message, ])
    send_main_th.start()
    print(threading.active_count())


# func for every time module
def main_mes(message):
    sch.every().day.at('09:10').do(main_inf)
    sch.every().day.at('20:10').do(main_inf)
    while True:
        sch.run_pending()
        time.sleep(1)


# func for checking message from user
def checking_text(message):
    error = 0
    ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
    rus_letters = 'ёйцукегншщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
    for letter in message.text:
        if letter in ascii_letters or letter in digits or letter in punctuation or letter in rus_letters or letter == '\n':
            pass
        else:
            error += 1
    if error == 0:
        return True
    else:
        return False


#   func for append note in data
def add_note_begin(message):
    # open json
    with open('data.json', 'r') as file_obj:
        data_from_json = json.load(file_obj)
    # get user id for send message
    user_id = message.from_user.id
    name = data_from_json[f'{user_id}']['username']
    bot.send_message(message.chat.id, f'{name}, пожалуйста введте текст заметки')
    bot.register_next_step_handler(message, add_note_end)


def add_note_end(message):
    # open json
    if checking_text(message):
        with open('data.json', 'r') as file_obj:
            data_from_json = json.load(file_obj)
        # get user`s inf
        user_id = message.from_user.id
        note_text = str(message.text)
        data_from_json[f'{user_id}']['note_text'] += f'\n{note_text}'
        with open('data.json', 'w') as file_obj:
            json.dump(data_from_json, file_obj, indent=4, ensure_ascii=False)
        bot.send_message(message.chat.id, f'Хорошо, я добавила заметку:\n "{data_from_json[f"{user_id}"]["note_text"]}" ')
        keyboard_work(message)
    else:
        bot.send_message(message.chat.id, f'Пожалуйста используйте только буквы, цифры и спец.символы')


# func for watch note
def watch_note(message):
    with open('data.json', 'r') as file_obj:
        data_from_json = json.load(file_obj)
    user_id = message.from_user.id
    name = data_from_json[f'{user_id}']['username']
    note = data_from_json[f'{user_id}']['note_text']
    bot.send_message(message.chat.id, f'{name}, вот ваша заметка:\n {note}')
    keyboard_work(message)


# func for del note
def delete_note(message):
    # open json
    with open('data.json', 'r') as file_obj:
        data_from_json = json.load(file_obj)
    # get user id for send message
    user_id = message.from_user.id
    name = data_from_json[f'{user_id}']['username']
    data_from_json[f'{user_id}']['note_text'] = ''
    with open('data.json', 'w') as file_obj:
        json.dump(data_from_json, file_obj, indent=4, ensure_ascii=False)
    bot.send_message(message.chat.id, f'{name}, я удалила Ваши заметки')
    keyboard_work(message)


# func for append schedule in data
def add_schedule_begin(message):
    # open json
    with open('data.json', 'r') as file_obj:
        data_from_json = json.load(file_obj)
    # get user id for send message
    user_id = message.from_user.id
    name = data_from_json[f'{user_id}']['username']
    bot.send_message(message.chat.id, f'{name}, пожалуйста введте текст расписания')
    bot.register_next_step_handler(message, add_schedule_end)


def add_schedule_end(message):
    if checking_text(message):
        # open json
        with open('data.json', 'r') as file_obj:
            data_from_json = json.load(file_obj)
        # get user`s inf
        user_id = message.from_user.id
        schedule_text = str(message.text)
        data_from_json[f'{user_id}']['schedule_text'] = f'{schedule_text}'
        with open('data.json', 'w') as file_obj:
            json.dump(data_from_json, file_obj, indent=4, ensure_ascii=False)
        bot.send_message(message.chat.id, f'Хорошо, я добавила изменила расписание:\n "{data_from_json[f"{user_id}"]["schedule_text"]}" ')
        keyboard_work(message)
    else:
        bot.send_message(message.chat.id, f'Пожалуйста используйте только буквы, цифры и спец.символы')


# func for watch note
def watch_schedule(message):
    with open('data.json', 'r') as file_obj:
        data_from_json = json.load(file_obj)
    user_id = message.from_user.id
    name = data_from_json[f'{user_id}']['username']
    schedule = data_from_json[f'{user_id}']['schedule_text']
    bot.send_message(message.chat.id, f'{name}, вот Ваше расписание:\n{schedule}')
    keyboard_work(message)


# func for edit appeal
def edit_appeal_begin(message):
    # open json
    with open('data.json', 'r') as file_obj:
        data_from_json = json.load(file_obj)
    # get user id for send message
    user_id = message.from_user.id
    name = data_from_json[f'{user_id}']['username']
    bot.send_message(message.chat.id, f'{name}, пожалуйста введите приятное для Вас обращение:')
    bot.register_next_step_handler(message, edit_appeal_end)


def edit_appeal_end(message):
    if checking_text(message):
        # open json
        with open('data.json', 'r') as file_obj:
            data_from_json = json.load(file_obj)
        # get user`s inf
        user_id = message.from_user.id
        appeal_text = str(message.text)
        data_from_json[f'{user_id}']['username'] = f'{appeal_text}'
        with open('data.json', 'w') as file_obj:
            json.dump(data_from_json, file_obj, indent=4, ensure_ascii=False)
        bot.send_message(message.chat.id, f'Хорошо, я теперь я буду обращаться к Вам: "{data_from_json[f"{user_id}"]["username"]}" ')
        keyboard_work(message)
    else:
        bot.send_message(message.chat.id, f'Пожалуйста используйте только буквы, цифры и спец.символы')


# func keyboard_work using very often
# it`s main keyboard
def keyboard_work(message):
    keyboard1 = tl.types.ReplyKeyboardMarkup(True, True, True)
    keyboard1.row('📰Информация', '📋Сводка', '📓Меню', '⚙Настройка')
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=keyboard1)


# keyboard for chose setting
def keyboard_setting(message):
    keyboard2 = tl.types.ReplyKeyboardMarkup(True, True, True)
    keyboard2.row('🗄Заметки', '📑Расписание', '👋Обращение')
    bot.send_message(message.chat.id, 'Что вы хотите изменить?', reply_markup=keyboard2)


# keyboard for menu
def keyboard_menu(message):
    keyboard4 = tl.types.ReplyKeyboardMarkup(True, True, True)
    keyboard4.row('🗄см.Заметки', '📑см.Расписание', '👋см.Обращение')
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=keyboard4)


# keyboard for notes
def keyboard_notes(message):
    keyboard5 = tl.types.ReplyKeyboardMarkup(True, True, True)
    keyboard5.row('➕Добавить', '➖Удалить')
    bot.send_message(message.chat.id, 'Вы можете добавить или удалить заметку.\n'
                                      'Прошу обратить внимание, что на кажго пользователя есть всего один слот!', reply_markup=keyboard5)


# keyboard for schedule
def keyboard_schedule(message):
    keyboard5 = tl.types.ReplyKeyboardMarkup(True, True, True)
    keyboard5.row('➕Изменить', '➖Убрать')
    bot.send_message(message.chat.id, 'Вы можете изменить или убрать раписание.\n'
                                      'Прошу обратить внимание, что на кажго пользователя есть всего один слот!', reply_markup=keyboard5)


# message handler
# start mes
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, get_inf())
    bot.send_message(message.chat.id, "Привет ✌, для корректной работы бота введите /reg")


# create new threading(admin func)
# !using only ofter run bot!
@bot.message_handler(commands=['admin_start_bot'])
def start_message(message):
    create_th(message)
    bot.send_message(message.chat.id, "Бот запущен и создал поток работы")
    # write logs
    with open('logs.txt', 'a+') as logs_obj:
        print(f'{message.from_user.id} - using admin func at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', file=logs_obj)
        logs_obj.close()


# register user in data
@bot.message_handler(commands=['reg'])
def start_message(message):
    # open JSON file
    with open('data.json', 'r') as file_obj:
        data_from_json = json.load(file_obj)
    # standard setting of user
    user_id = message.from_user.id
    username = message.from_user.username
    schedule_text = 'Пусто'
    note_text = ''
    # check user.id
    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {"username": username, "schedule_text": schedule_text,
                                   "note_text": note_text}
    # append user in json
    with open('data.json', 'w') as file_obj:
        json.dump(data_from_json, file_obj, indent=4, ensure_ascii=False)
    bot.send_message(message.chat.id, f"Вы зарегистрированы "
                                      f"Ваш user_id {user_id}, теперь вы можете изменить настойки под себя")
    keyboard_work(message)

    # write logs
    with open('logs.txt', 'a+') as logs_obj:
        print(f'{user_id} - reg in bot at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', file=logs_obj)
        logs_obj.close()
    print(threading.active_count())


@bot.message_handler(content_types=['text'])
def main_message(message):
    # get inf by user
    if message.text == '📰Информация':
        bot.send_message(message.chat.id, get_inf())
        keyboard_work(message)
    # report
    elif message.text == '📋Сводка':
        bot.send_message(message.chat.id, 'Меня зовут AsunaBot, я создана для оптимизации вашей ежедневной рутины,'
                                          ' связанной с поиском информации, моя цель - делать вашу жизнь проще и интересней.'
                                          ' Что я могу?\nДва раза в день я автоматически высылаю Вам сжатую информацию, что бы Вы были в курсе всех основных событий.'
                                          ' Так же я могу хранить Выши заметки и расписание, которое Вы можете в любой момент изменить или удалить.\n'
                                          'Спасибо, что Вы доверились именно мне. В бедущем мой создатель добавит ещё много полезных функций!😸')
        bot.send_message(message.chat.id, 'Кстати один из переводов моего имени(Asuna) - "завтра", очень символьчно, не так ли?')
    # setting
    elif message.text == '⚙Настройка':
        keyboard_setting(message)
    # appeal
    elif message.text == '👋Обращение':
        edit_appeal_begin(message)
    # menu
    elif message.text == '📓Меню':
        keyboard_menu(message)
    # note
    elif message.text == '🗄Заметки':
        keyboard_notes(message)
    elif message.text == '➕Добавить':
        add_note_begin(message)
    elif message.text == '🗄см.Заметки':
        watch_note(message)
    elif message.text == '➖Удалить':
        delete_note(message)
    # schedule
    elif message.text == '📑Расписание':
        keyboard_schedule(message)
    elif message.text == '➕Изменить':
        add_schedule_begin(message)
    elif message.text == '📑см.Расписание':
        watch_schedule(message)


bot.polling()
print(threading.active_count())
