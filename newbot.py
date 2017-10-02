import json
import config
import telebot
import sqlite3
import requests
import uuid
from telebot import types
import time

tasks = ['Сколько в 1 кубическом метре кубических сантиметров? Запишите только число',
         'Сколько яблок в среднем растёт на вишне? Напишите только число(их количество)',
         'Машина весит 1 тонну. Каккова сила тяжести машины? ' \
         'Ускорение свободного падения принять за 10 м/с^2. Напишите только число.',
         'Записать в секундах одну шестую часа. Записать только число.',
         'Определите массу 1 моль водорода.',
         'Напишите год основания Руси.',
         'Сколько месяцев в году имеют 28 дней? Напишите число.',
         "Сколько будет 2+2*2?",
         "Напишите минимальное значение функции y=2x^2+14x+7",
         'Дюжина - это сколько?',
         'У квадратного стола отпилили один угол по прямой линии . Сколько теперь углов у стола?',
         'Запишите число 8 в двоичной системе счисления.']

answers = [1000000000, 0, 10000, 600, 0.002, 862, 12, 6, 7, 12, 5, 1000]

bot = telebot.TeleBot(config.token)

r = 0
w = 0
password = ['r000', 'r001', 'r002', 'w000', 'w001', 'w002']
users = {}
users = dict([(0, ' '), (1, -1), (2, ' '), (3, -1)])


@bot.message_handler(commands=['Vlad'])
def Vlad(message):
    k = bot.send_message(message.chat.id, 'Здорово, хозяин. Напиши б, для перехода к тесту')
    bot.register_next_step_handler(k, task_handler)
# users[0] - пароль, users[1] - место в массиве паролей, users[2] - имя
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('Для продолжентя нажмите на эту кнопку')
    gh = bot.send_message(message.chat.id, 'От имени своего создателя приветсвую вас в Catch the Flag или сокращённо '
                                           'в CTF.'
                                           ' Зовите меня Макс. Ну что ж, начнём!', reply_markup=markup)
    bot.register_next_step_handler(gh, starting_handler)


@bot.message_handler(commands=['newpass'])
def starting_handler(message):
    if users[0] == password[users[1]]:
        m = bot.send_message(message.chat.id, "Вы в игре, можете продолжать.")
        bot.register_next_step_handler(m, name_handler)
    else:
        ans = bot.send_message(message.chat.id, 'Введите ваш пароль, пожалуйста.')
        bot.register_next_step_handler(ans, password_handler)


def password_handler(message):
    if users[0] == password[users[1]]:
        lc = bot.send_message(message.chat.id, "Вы в игре, можете продолжать.")
        bot.register_next_step_handler(lc, name_handler)
    else:
        users[0] = message.text
        if users[0] == "Иллюзион":
            bot.send_message(message.chat.id, 'Время вышло.')
            if r > w:
                bot.send_message(message.chat.id, 'Выиграла Красная команда со счётом {r} против Белой команды, '
                                                  'набравшей {w},'
                                                  'очков. Мой создатель поздравляет победителей с их достижением. '
                                                  'Ждём вас снова '
                                                  ' в Catch the Flag. '
                                                  'До скорого!'.format(r=r, w=w))
            elif w > r:
                bot.send_message(message.chat.id, 'Выиграла Белая команда со счётом {w} против Красной команды, '
                                                  'набравшей {r}'
                                                  ' очков. Мой создатель поздравляет победителей с их достижением. '
                                                  'Ждём вас снова в Catch the Flag. До скорого!'.format(r=r, w=w))
            elif w == r:
                bot.send_message(message.chat.id, 'Вот это да! Удивительно, но у нас ничья: {r}:{w},'
                                                  'Победила дружба, товарищи-игроки! Мой создатель благодарит всех за '
                                                  'участие в его проекте. Ждём вас снова в Catch the Flag. До '
                                                  'скорого!'.format(r=r, w=w))
        for i in range(0, 6):
            if users[0] == password[i]:
                users[1] = i
                gop = bot.send_message(message.chat.id, 'Ваш пароль верный. '
                                                        'Для конечной авторизации напишите  команду continue')
                bot.register_next_step_handler(gop, name_handler)
            i += 1
        if users[1] == -1:
            lo = bot.send_message(message.chat.id, 'Вашего пароля нет в базе данных. Наверное, вы ошиблись. '
                                                   'Для введения нового пароля кликните /newpass')
            bot.register_next_step_handler(lo, starting_handler)


@bot.message_handler(commands=['continue'])
def name_handler(message):
    l = bot.send_message(message.chat.id, 'Введите ваши имя и фамилию, пожалуйста(только, умаляю, настоящие '
                                          'и без всяких никнеймов а-ля Givoglot, EstonianNinja, N.E.C. и т.д.)')
    bot.register_next_step_handler(l, endless)


def endless(message):
    global b
    b = time.time()
    users[2] = message.text
    intro = bot.send_message(message.chat.id,
                             'Теперь, {name}, ты полностью авторизован. Двигайся к своему первому Qr-коду,'
                             ' сфотографируй его и пришли фото мне.'.format(name=message.text))
    bot.register_next_step_handler(intro, task_handler)


@bot.message_handler(content_types=['photo'])
def task_handler(message):
    file_id = message.photo[-1].file_id
    path = bot.get_file(file_id)
    p = 'https://api.telegram.org/file/bot{0}/'.format(config.token) + path.file_path
    url = 'http://api.qrserver.com/v1/read-qr-code/'
    res = requests.post(url, {'fileurl': p})
    global x
    try:
        x = int(res.json()[0]['symbol'][0]['data'])
        users[3] = x
        pila = bot.send_message(message.chat.id, tasks[x])
        bot.register_next_step_handler(pila, answer_handler)
    except:
        bot.send_message(message.chat.id, 'Извините, не смог распознать код. Пришли новый, {name}.'
                                .format(name=users[2]))

def answer_handler(message):
    answer = message.text
    if answer == str(answers[users[3]]):
        bot.send_message(message.chat.id, 'Ваш ответ верен. Мои поздравления!')
        conn = sqlite3.connect('noble.sqlite')
        c = conn.cursor()
        rows = c.execute('select * from noble').fetchall()
        conn.commit()
        rows = list(rows)
        rows[0] = list(rows[0])
        if users[1] <= 2:
            c.execute('DELETE FROM noble WHERE rowid=1')
            rows[0][0] += 1
            c.executemany('insert into noble values(?,?)', rows)
            conn.commit()
        if users[1] >= 3:
            c.execute('DELETE FROM noble WHERE rowid=1')
            rows[0][1] += 1
            c.executemany('insert into noble values(?,?)', rows)
            conn.commit()
        c.close()
    else:
        bot.send_message(message.chat.id, 'Ваш ответ неправильный. Мне жаль.')
    bot.send_message(message.chat.id, 'Отправляйся к следующему QR-коду и пришли его фотографию.')


bot.polling(none_stop=True)
