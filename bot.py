import random
import re
import sqlite3
import asyncio
import os
import datetime
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from dotenv import load_dotenv, find_dotenv

admin_id = 1900666417

load_dotenv(find_dotenv())
bot = AsyncTeleBot(os.getenv('TOKEN_BOT'))

db = sqlite3.connect('db/fnaf.db', check_same_thread=False)
sql = db.cursor()

# Создание двух таблиц users и download
sql.execute("""CREATE TABLE IF NOT EXISTS download(
    id integer PRIMARY KEY AUTOINCREMENT,
    tg_id integer,
    link text,
    date date


)""")

sql.execute("""CREATE TABLE IF NOT EXISTS users(
    id integer PRIMARY KEY AUTOINCREMENT,
    tg_id integer,
    username text,
    utm text,
    date date
)""")



db_tiktok = sqlite3.connect('~TTsavee/db/ttsavee.db', check_same_thread=False)
db_insta = sqlite3.connect('~korzu/InstaSavee/db/instasavee.db', check_same_thread=False)

def checkSubscribe(tg_id, db):
    sql = db.cursor()

    sql.execute("SELECT * FROM users WHERE tg_id = $1;", tg_id)

    user = sql.fetchone()

    sql.close()

    if user:
        return True
    else:
        return False


async def all_bot(chat_id,message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_1 = types.InlineKeyboardButton(text="Скачать видео из TikTok", url="https://t.me/saving_tt_video_bot?start=Fnaf")
    button_2 = types.InlineKeyboardButton(text="Скачать видео из Instagram",url="https://t.me/saving_insta_bot?start=Fnaf")

    markup.add(button_1,button_2)

    await bot.send_message(message.chat.id,
                           'Для того что бы узнать кто ты из FNAF, тебе так же нужно подписаться на наших ботов',reply_markup=markup)


# Команда для админа которая делает рассылку по всем пользователям из базы данных
@bot.message_handler(commands=['sendall'])
async def send_all_message(message: types.Message):
    sql.execute("SELECT tg_id FROM users;")
    users = sql.fetchall()
    if message.chat.id == admin_id:
        await bot.send_message(message.chat.id, '💌 Starting')
        for i in users:
            try:
                print("Send to: ", str(i[0]))
                await bot.send_message(i[0], message.text[message.text.find(' '):], parse_mode='html')
            except Exception as error:
                print("Blocked bot: ", str(i[0]))
            # await bot.send_message(i[0],message.text[message.text.find(' '):],parse_mode='html')
        await bot.send_message(message.chat.id, '✅ Successfully')
    else:
        await bot.send_message(message.chat.id, 'Вы не являетесь администратором!')


# Команда для админа которая скачивает с сервера базу данных
@bot.message_handler(commands=['download_db'])
async def command_download_db(message):
    if message.chat.id == admin_id:
        db = open('db/fnaf.db', 'rb')
        await bot.send_document(message.chat.id, db)
    else:
        await bot.send_message(message.chat.id, 'Вы не являетесь администратором!')

@bot.message_handler(commands=['users'])
async def all_users(message):
    if message.chat.id == admin_id:
        sql.execute("SELECT tg_id FROM users;")
        users = sql.fetchall()
        await bot.send_message(message.chat.id, f'👻 Общее количество пользователей: <b>{len(users)}</b>',
                               parse_mode='html')
    else:
        await bot.send_message(message.chat.id, f'🚫 Вы не является администратором')

name = ['😱 Оказывается ты Фредди! ', '😱 Оказывается ты Бонни!', '😱 Оказывается ты Чика!', '😱 Оказывается ты Фокси!',
        '😱 Оказывается ты Золотой Фредди!', '😱 Оказывается ты Марионетка!', '😱 Оказывается ты Балун Бой!',
        '😱 Оказывается ты Спрингтрап!', '😱 Оказывается ты Мангл!', '😱 Оказывается ты Циркус Бэби!',
        '😱 Оказывается ты Эннард!', '😱 Оказывается ты Баллора!', '😱 Оказывается ты Уильям Афтон!']

photo = ['img/freddy.jpg', 'img/bonny.jpg', 'img/chika.jpg', 'img/foxy.jpg', 'img/golden_freddy.jpg',
         'img/marionetka.jpg', 'img/balunboy.jpg', 'img/springtrap.jpg', 'img/mangl.jpg', 'img/cirk_baby.jpg',
         'img/ennar.jpg', 'img/ballora.jpg', 'img/aftin.jpg']

characters = dict(zip(name, photo))


@bot.message_handler(commands=['start'])
async def command_start(message):
    utm_label = (message.text).split(' ')

    print(len(utm_label))
    if len(utm_label) >= 2:
        utm = utm_label[1]
    else:
        utm = 'hull'

    date = datetime.datetime.now()
    tg_id = message.from_user.id
    sql.execute(f"SELECT tg_id FROM users WHERE tg_id={tg_id}")
    data = sql.fetchone()
    username = message.from_user.username

    sql.execute("SELECT tg_id FROM download;")
    quantity_download = sql.fetchall()
    if data is None:

        if message.from_user.username != None:
            await bot.send_message(admin_id, f'👤 New user : @{message.from_user.username} {message.chat.id}')
        else:
            await bot.send_message(admin_id, f'👤 New user : {message.chat.id}')


        if username != None:

            sql.execute("INSERT INTO users VALUES (?,?,?,?,?)", (None, tg_id, username, utm, date))
            db.commit()
        else:
            username_none = 'Stranger'
            sql.execute("INSERT INTO users VALUES (?,?,?,?,?)", (None, tg_id, username_none, utm, date))
            db.commit()

    with open('img/start.png', 'rb') as start_photo:
        await bot.send_photo(message.chat.id, start_photo,
                             'Привет! Я бот <b>Кто ты из FNaF?</b> 🐻🐰🦊\n\nДля этого мне понадобится твоя дата рождения. Пожалуйста, введи дату своего рождения в формате <b>ДД.ММ.ГГГГ</b> (например, 31.10.1990).\n\nПосле того как ты введешь свою дату рождения, я скажу, кто ты из персонажей FNaF.\n\n<b>Готов начать? Введи свою дату рождения!</b>',
                             parse_mode='html')


@bot.message_handler(content_types=['text'])
async def message_handler(message):
    checkSubscribe(message.chat.id, db_tiktok)
    if checkSubscribe == True:
        if re.match(r'\d{2}.\d{2}.\d{4}', message.text):
                if message.from_user.username != None:
                    await bot.send_message(admin_id,
                                               f'<b>Username: @{message.from_user.username}</b>\n<b>👤 User id:</b> {message.chat.id}\n<b>⛓ text</b>: <code>{message.text}</code>\n<b>🟢 Status:</b> 📩 Link accepted!',
                                               parse_mode='html')
                else:
                    await bot.send_message(admin_id,
                                               f'<b>👤 User:</b> {message.chat.id}\n<b>⛓text</b>: <code>{message.text}</code>\n<b>🟢 Status:</b> 📩 Link accepted!',
                                               parse_mode='html')

                random_name = random.choice(name)

                random_photo = characters[random_name]
                with open(f'{random_photo}', 'rb') as photo:

                    await bot.send_photo(message.chat.id, photo, f'<b>{random_name}</b>\n\nВаша связь с этим персонажем может быть ключом к раскрытию секретов игры и пониманию её сюжета. Приготовьтесь к захватывающему и опасному приключению, где вы будете играть важную роль.\n\n<b>🌟Удачи в этой увлекательной игре!</b>',
                                         parse_mode='html')
                    words = random_name.split()
                    last_word = words[-1]
                    inline_keyboard = types.InlineKeyboardMarkup()
                    share_button = types.InlineKeyboardButton("Поделиться", switch_inline_query=f'Помог мне узнать кто я из FNaF.\n\n😱 Как оказалось я {last_word}')

                    inline_keyboard.add(share_button)

                    await bot.send_message(message.chat.id, "Скорее делись результатом  со своими друзьями! 🐻🐰🦊",
                                           reply_markup=inline_keyboard)
                date = datetime.datetime.now()
                tg_id = message.from_user.id
                link = message.text
                sql.execute("INSERT INTO download VALUES (?,?,?,?)", (None, tg_id, link, date))
                db.commit()
        else:
            await bot.send_message(message.chat.id, 'Пожалуйста, введите дату в формате гггг-мм-дд.')
    else:
        await all_bot(message.chat.id,message)
asyncio.run(bot.polling(non_stop=True))
