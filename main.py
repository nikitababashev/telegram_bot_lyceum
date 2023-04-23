import logging
from PIL import Image
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import sqlite3
import telegram
import telebot
import requests
from io import BytesIO
from datetime import datetime
from urllib.parse import quote
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)
con = sqlite3.connect('db/user_stat.db')
cur = con.cursor()
check_registration_users = []
API_URL = 'https://api.mymemory.translated.net/get?q={}&langpair=en|ru'
bot = telebot.TeleBot('6036045502:AAEN6Wb7h18Kfle3YDfropM7ZqIawZhH10c')
bot_t = telegram.Bot(token='6036045502:AAEN6Wb7h18Kfle3YDfropM7ZqIawZhH10c')
questions_oge_eazy = [
    {"image": "images/oge_eazy/1.jpg",
     "question": "Было проведено 9 запусков программы,"
                 " при которых в качестве значений"
                 " переменных s и t вводились следующие пары чисел:\n"
                 "(1, 2); (11, 2); (1, 12); (11, 12); "
                 "(–11, –12); (–11, 12); (–12, 11); (10, 10); (10, 5).\n"
                 "Сколько было запусков, при которых программа напечатала «YES»?",
     "answer": "5"},
    {"image": "images/oge_eazy/2.jpg",
     "question": "Было проведено 9 запусков программы,"
                 " при которых в качестве значений"
                 " переменных s и t вводились следующие пары чисел:\n"
                 "(1, 13); (14, 2); (1, 12); (11, 12); "
                 "(–14, –14); (–11, 13); (–4, 11); (2, 9); (8, 6).\n"
                 "Сколько было запусков, при которых программа напечатала «YES»?",
     "answer": "3"},
    {"image": "images/oge_eazy/3.jpg",
     "question": "Было проведено 9 запусков программы,"
                 " при которых в качестве значений переменных"
                 " s и t вводились следующие пары чисел:\n"
                 "(3, 4); (5, 4); (–2, 1); (5, 6); (7, 8); (–5, 5); (–2, 2); (4, 3); (12, 22).\n"
                 "Сколько было запусков, при которых программа напечатала «NO»?",
     "answer": "4"}
]
questions_oge_medium = [
    {"image": "images/oge_medium/1.jpg",
     "question": "Было проведено 9 запусков программы,"
                 " при которых в качестве значений переменных "
                 "s и k вводились следующие пары чисел:\n"
                 "(1, 1); (8, 4); (14, 10); (20, 1); (7, 3); (10, 5); (10, 2); (4, 1); (1, 0).\n"
                 "Сколько было запусков, при которых программа напечатала «ДА»?",
     "answer": "4"},
    {"image": "images/oge_medium/2.jpg",
     "question": "Было проведено 9 запусков программы, "
                 "при которых в качестве значений переменных "
                 "s и k вводились следующие пары чисел:\n"
                 "(1, 2); (8, 4); (6, −12); (−5, −5); "
                 "(3, 11); (—10, 12); (—10, −2); (4, 1); (2, 5).\n"
                 "Сколько было запусков, при которых программа напечатала «ДА»?",
     "answer": "4"},
    {"image": "images/oge_medium/3.jpg",
     "question": "Было проведено 9 запусков программы,"
                 " при которых в качестве значений переменных"
                 " s и t вводились следующие пары чисел:\n"
                 "(–2, 3); (2, 5); (0, 3); (5, –3); (5, 4); (11, 4); (8, –6); (7, 3); (9, 1).\n"
                 "Сколько было запусков, при которых программа напечатала «YES»?",
     "answer": "6"}
]
questions_oge_hard = [
    {"image": "images/oge_hard/1.jpg",
     "question": "Какой знак нужно поставить, чтобы получился верный ответ?\n"
                 "Входные данные:\n"
                 "      3\n"
                 "      12\n"
                 "      25\n"
                 "      6\n"
                 "Выходные данные:\n"
                 "      18",
     "answer": "%"},
    {"image": "images/oge_hard/2.jpg",
     "question": "Какой оператор нужно поставить, чтобы получился верный ответ?\n"
                 "Входные данные:\n"
                 "      1\n"
                 "      20\n"
                 "      21\n"
                 "      30\n"
                 "      0\n"
                 "Выходные данные:\n"
                 "      4\n"
                 "      50\n",
     "answer": "and"},
    {"image": "images/oge_hard/3.jpg",
     "question": "Какое значение нужно поставить, чтобы получился верный ответ?\n"
                 "Входные данные:\n"
                 "      18\n"
                 "      21\n"
                 "      28\n"
                 "      18\n"
                 "      0\n"
                 "Выходные данные:\n"
                 "      36",
     "answer": "8"}
]
questions_used = []


async def start(update, context):
    check_registration_users_db = cur.execute("""SELECT id_users FROM statistics""").fetchall()
    for id_user_db in check_registration_users_db:
        check_registration_users.append(id_user_db[0])
    if update.message.chat.id in check_registration_users:
        name_in_db = cur.execute(f"""SELECT really_name FROM statistics
                                WHERE id_users = {update.message.chat.id}""").fetchall()
        context.user_data['name'] = name_in_db[0][0]
        reply_keyboard = [['практика', 'теория']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(f"Приятно снова видеть тебя с нами,"
                                        f" {context.user_data['name']}!\n"
                                        f"С тобой по-прежнему дружелюбный Бот-Кеша!\n"
                                        f"С чего хочешь начать, практика или теория?\n"
                                        f"*не забывай про имеющиеся команды:\n"
                                        f"/sdialog - остановить бота в любое время"
                                        f" и начать диалог заново, написав /start\n"
                                        f"/profile - посмотреть свой профиль*",
                                        reply_markup=markup)
        return 'distribution'
    else:
        await update.message.reply_text('Привет! Как тебя зовут?',
                                        reply_markup=ReplyKeyboardRemove())
        return 'start_dialog'


async def first_response(update, context):
    context.user_data['id_user'] = update.message.chat.id
    context.user_data['name'] = update.message.text
    if context.user_data['name'] == update.message.chat.first_name:
        reply_keyboard = [['практика', 'теория']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        cur.execute(f"""INSERT INTO statistics(id_users, really_name)
                        VALUES({context.user_data['id_user']}, '{context.user_data['name']}')""")
        con.commit()

        await update.message.reply_text(f"Приятно познакомиться, {context.user_data['name']}!\n"
                                        f"Чтобы я мог запомнить тебя, вызови команду "
                                        f"/create_profile_user, эта функция создаcт твой личный"
                                        f" профиль.\n"
                                        f"Посмотреть его можно через команду - /profile\n"
                                        f"Меня зовут Бот-Кеша.\n"
                                        f"Хочешь ли ты попробовать попрактиковаться в решение задач"
                                        f" из огэ или егэ по программированию?\n"
                                        f"Или же изначально ты хочешь прочитать теорию?\n"
                                        f"Чтобы выбрать, напиши: практика / теория\n"
                                        f"*также ты можешь остановить бота в любое время с "
                                        f"помощью команды - /sdialog*", reply_markup=markup)
        return 'distribution'
    else:
        await update.message.reply_text(f"Мне кажется, что ты хочешь меня обмануть!\n"
                                        f"Думаю, что тебя зовут {update.message.chat.first_name}"
                                        f", а не {context.user_data['name']}!\n"
                                        f"Верно?")
        return 'distribution_fr'


async def distribution_fr(update, context):
    answer = update.message.text.lower()
    if answer == 'да' or answer == 'верно':
        reply_keyboard = [['практика', 'теория']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        context.user_data['fake_name'] = context.user_data['name']
        context.user_data['name'] = update.message.chat.first_name

        cur.execute(f"""INSERT INTO statistics(id_users, really_name, fake_nickname)
                        VALUES({context.user_data['id_user']}, '{context.user_data['name']},
                         '{context.user_data['fake_name']}')""")
        con.commit()

        await update.message.reply_text(f"Мы - боты, развитые объекты, нас не так-то просто "
                                        f"обмануть!\n"
                                        f"Приятно познакомиться,"
                                        f" {context.user_data['name']}!\n"
                                        f"Чтобы я мог запомнить тебя, вызови команду "
                                        f"/create_profile_user, эта функция создаcт твой личный"
                                        f" профиль.\n"
                                        f"Посмотреть его можно через команду - /profile\n"
                                        f"Меня зовут Бот-Кеша.\n"
                                        f"Хочешь ли ты попробовать попрактиковаться в решение задач"
                                        f" из огэ или егэ по программированию?\n"
                                        f"Или же изначально ты хочешь прочитать теорию?\n"
                                        f"Чтобы выбрать, напиши: практика / теория\n"
                                        f"*также ты можешь остановить бота в любое время с "
                                        f"помощью команды - /sdialog*", reply_markup=markup)
        return 'distribution'
    elif answer == 'нет' or answer == 'не верно':
        reply_keyboard = [['практика', 'теория']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        cur.execute(f"""INSERT INTO statistics(id_users, really_name)
                        VALUES({context.user_data['id_user']}, '{context.user_data['name']}')""")
        con.commit()

        await update.message.reply_text(f"Прошу прощения, мы - боты, еще не до конца развиты!\n"
                                        f"Приятно познакомиться, {context.user_data['name']}!\n"
                                        f"Чтобы я мог запомнить тебя, вызови команду "
                                        f"/create_profile_user, эта функция создаcт твой личный"
                                        f" профиль.\n"
                                        f"Посмотреть его можно через команду - /profile\n"
                                        f"Меня зовут Бот-Кеша.\n"
                                        f"Хочешь ли ты попробовать попрактиковаться в решение задач"
                                        f" из огэ или егэ по программированию?\n"
                                        f"Или же изначально ты хочешь прочитать теорию?\n"
                                        f"Чтобы выбрать, напиши: практика / теория\n"
                                        f"*также ты можешь остановить бота в любое время с "
                                        f"помощью команды - /sdialog*", reply_markup=markup)
        return 'distribution'
    else:
        await update.message.reply_text(f"Извини, но я тебя не понимаю.\n"
                                        f"Ответь, пожалуйста, в формате: да / нет")
        return 'distribution_fr'


async def distribution(update, context):
    answer = update.message.text.lower()

    if answer == 'практика':

        cur.execute(f"""UPDATE statistics SET count_practice = count_practice + 1
                    WHERE id_users = {update.message.chat.id}""")
        con.commit()

        reply_keyboard = [['ОГЭ', 'ЕГЭ'], ['практика/теория']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False,
                                     input_field_placeholder="любим гусей!")
        if update.message.chat.id in check_registration_users:
            await update.message.reply_text('Хорошо, вижу, что ты также уверен в своих силах,'
                                            ' как и в прошлый раз!\n'
                                            'Выбери из какого экзамена ты хочешь порешать задачи.',
                                            reply_markup=markup)
        else:
            await update.message.reply_text('Хорошо, вижу, что ты уверен(а) в своих силах!\n'
                                            'Выбери из какого экзамена ты хочешь порешать задачи.',
                                            reply_markup=markup)
        return 'distribution_oge_or_ege'
    if answer == 'теория':
        cur.execute(f"""UPDATE statistics SET count_theory = count_theory + 1
                    WHERE id_users = {update.message.chat.id}""")
        con.commit()

        reply_keyboard = [['перейти к практике'], ['переводчик']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        await update.message.reply_text(f"Теория не менее важна, чем практика!\n"
                                        f"Ознакомиться с теорией можешь на нашем сайте:\n"
                                        f"      https://lyceum.yandex.ru/courses/766/groups/5718",
                                        reply_markup=markup)
        return 'distribution_after_theory'


async def distribution_after_theory(update, context):
    answer = update.message.text.lower()
    if answer == 'переводчик':
        await update.message.reply_text('Чтобы уметь программировать нужно хорошо знать'
                                        ' английский.\n'
                                        'Сейчас вы можете прислать мне текст на английском и я'
                                        ' переведу его на русский, пока что я '
                                        'не умею переводить с русского на английский.\n'
                                        'Чтобы закрыть переводчик, введите слово - "закрыть"\n'
                                        'Напишите текст на английском:',
                                        reply_markup=ReplyKeyboardRemove())
        return 'translate_text'
    elif answer == 'перейти к практике':

        cur.execute(f"""UPDATE statistics SET count_practice = count_practice + 1
                    WHERE id_users = {update.message.chat.id}""")
        con.commit()

        reply_keyboard = [['ОГЭ', 'ЕГЭ']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False,
                                     input_field_placeholder="любим гусей!")
        await update.message.reply_text('Хорошо, вижу, что ты уверен(а) в своих силах!\n'
                                        'Выбери из какого экзамена ты хочешь порешать задачи.',
                                        reply_markup=markup)
        return 'distribution_oge_or_ege'


async def translate_text(update, context):
    text = update.message.text
    if text == 'закрыть':
        reply_keyboard = [['практика', 'теория']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text('Вы закрыли переводчик.\n'
                                        'Переношу вас в изначальный пункт выбора!',
                                        reply_markup=markup)
        return 'distribution'
    else:
        url = API_URL.format(quote(text))
        response = requests.get(url)
        translation = response.json()['responseData']['translatedText']
        await update.message.reply_text(translation, reply_markup=ReplyKeyboardRemove())


async def distribution_oge_or_ege(update, context):
    answer = update.message.text
    if answer == 'практика/теория':
        reply_keyboard = [['практика', 'теория']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text('Выберите свой путь!', reply_markup=markup)
        return 'distribution'
    else:
        await update.message.reply_text('За каждый верный ответ будут начисляться баллы!\n'
                                        'ОГЭ:\n'
                                        '    лёгкий уровень сложности - 1 балл\n'
                                        '    средний уровень сложности - 2 балла\n'
                                        '    сложный уровень сложности - 3 балла\n'
                                        'ЕГЭ:\n'
                                        '    лёгкий уровень сложности - 4 балла\n'
                                        '    средний уровень сложности - 5 баллов\n'
                                        '    сложный уровень сложности - 6 баллов\n'
                                        'За каждый неверный ответ -1 балл!\n'
                                        'Баллы будут в вашем профиле - /profile')
        reply_keyboard = [['лёгкая', 'средняя', 'сложная'], ['практика/теория']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        if answer == 'ОГЭ':
            await update.message.reply_text('Вы выбрали - ОГЭ!\n'
                                            'Выберите сложность:\n'
                                            '1) лёгкая\n'
                                            '2) средняя\n'
                                            '3) сложная', reply_markup=markup)
            return 'distribution_oge'
        elif answer == 'ЕГЭ':
            await update.message.reply_text('Вы выбрали - ОГЭ!\n'
                                            'Выберите сложность:\n'
                                            '1) лёгкая\n'
                                            '2) средняя\n'
                                            '3) сложная', reply_markup=markup)
            return 'distribution_ege'


async def distribution_oge(update, context):
    global questions_used
    answer = update.message.text.lower()
    reply_keyboard = [['практика/теория']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False,
                                 input_field_placeholder="любим гусей!")
    questions_used = []
    if answer == '1' or answer == 'лёгкая':
        question = random.choice(questions_oge_eazy)
        img = question['image']
        quest = question['question']
        await update.message.reply_text('Лёгкий уровень сложности:',
                                        reply_markup=markup)
        bot.send_photo(update.message.chat.id, photo=open(img, 'rb'),
                       caption=quest)
        questions_used.append(question)
        return 'check_answer'
    if answer == '2' or answer == 'средняя':
        question = random.choice(questions_oge_medium)
        img = question['image']
        quest = question['question']
        await update.message.reply_text('Средний уровень сложности:',
                                        reply_markup=markup)
        bot.send_photo(update.message.chat.id, photo=open(img, 'rb'),
                       caption=quest)
        questions_used.append(question)
        return 'check_answer'
    if answer == '3' or answer == 'сложная':
        question = random.choice(questions_oge_hard)
        img = question['image']
        quest = question['question']
        await update.message.reply_text('Сложный уровень сложности:',
                                        reply_markup=markup)
        bot.send_photo(update.message.chat.id, photo=open(img, 'rb'),
                       caption=quest)
        questions_used.append(question)
        return 'check_answer'
    if answer == 'практика/теория':
        reply_keyboard = [['практика', 'теория']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text('Выберите свой путь!', reply_markup=markup)
        return 'distribution'


async def check_answer(update, context):
    reply_keyboard = [['практика/теория']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False,
                                 input_field_placeholder="любим гусей!")
    answer = update.message.text
    if answer == questions_used[-1]['answer']:
        if questions_used[-1] in questions_oge_eazy:

            cur.execute(f"""UPDATE statistics SET scores = scores + 1
                        WHERE id_users = {update.message.chat.id}""")
            con.commit()

            if len(questions_used) < 3:
                await update.message.reply_text('Правильно!\n'
                                                'Следующий тест:')
                while True:
                    question = random.choice(questions_oge_eazy)
                    if question not in questions_used:
                        break
                img = question['image']
                quest = question['question']
                await update.message.reply_text('Лёгкий уровень сложности:',
                                                reply_markup=markup)
                bot.send_photo(update.message.chat.id, photo=open(img, 'rb'),
                               caption=quest)
                questions_used.append(question)
                return 'check_answer'

            else:
                await update.message.reply_text('Правильно!\n'
                                                'Вы прошли все тесты лёгкой сложности.\n'
                                                'Переношу вас на средний уровень сложности!')
                question = random.choice(questions_oge_medium)
                img = question['image']
                quest = question['question']
                await update.message.reply_text('Средний уровень сложности:',
                                                reply_markup=markup)
                bot.send_photo(update.message.chat.id, photo=open(img, 'rb'),
                               caption=quest)
                questions_used.clear()
                questions_used.append(question)
                return 'check_answer'

        if questions_used[-1] in questions_oge_medium:

            cur.execute(f"""UPDATE statistics SET scores = scores + 2
                        WHERE id_users = {update.message.chat.id}""")
            con.commit()

            if len(questions_used) < 3:
                await update.message.reply_text('Правильно!\n'
                                                'Следующий тест:')
                while True:
                    question = random.choice(questions_oge_medium)
                    if question not in questions_used:
                        break
                img = question['image']
                quest = question['question']
                await update.message.reply_text('Средний уровень сложности:',
                                                reply_markup=markup)
                bot.send_photo(update.message.chat.id, photo=open(img, 'rb'),
                               caption=quest)
                questions_used.append(question)
                return 'check_answer'

            else:
                await update.message.reply_text('Правильно!\n'
                                                'Вы прошли все тесты средней сложности.\n'
                                                'Переношу вас на сложный уровень сложности!')
                question = random.choice(questions_oge_hard)
                img = question['image']
                quest = question['question']
                await update.message.reply_text('Сложный уровень сложности:',
                                                reply_markup=markup)
                bot.send_photo(update.message.chat.id, photo=open(img, 'rb'),
                               caption=quest)
                questions_used.clear()
                questions_used.append(question)
                return 'check_answer'

        if questions_used[-1] in questions_oge_hard:

            cur.execute(f"""UPDATE statistics SET scores = scores + 3
                        WHERE id_users = {update.message.chat.id}""")
            con.commit()

            if len(questions_used) < 3:
                await update.message.reply_text('Правильно!\n'
                                                'Следующий тест:')
                while True:
                    question = random.choice(questions_oge_hard)
                    if question not in questions_used:
                        break
                img = question['image']
                quest = question['question']
                await update.message.reply_text('Сложный уровень сложности:',
                                                reply_markup=markup)
                bot.send_photo(update.message.chat.id, photo=open(img, 'rb'),
                               caption=quest)
                questions_used.append(question)
                return 'check_answer'

            else:
                await update.message.reply_text('Правильно!\n'
                                                'Вы прошли все возможные тесты в разделе "ОГЭ"\n'
                                                'Вы можете вернуться, чтобы закрепить'
                                                ' материал.')
                reply_keyboard = [['практика', 'теория']]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                await update.message.reply_text('Куда вы хотите направиться?', reply_markup=markup)
                return 'distribution'

    elif answer == 'практика/теория':
        reply_keyboard = [['практика', 'теория']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text('Выберите свой путь!', reply_markup=markup)
        return 'distribution'

    else:

        cur.execute(f"""UPDATE statistics SET scores = scores - 1
                    WHERE id_users = {update.message.chat.id}""")
        con.commit()

        await update.message.reply_text('Вы ответили неверно!\n'
                                        'Попробуйте еще раз!', reply_markup=markup)
        return 'check_answer'


async def distribution_ege(update, context):
    answer = update.message.text.lower()
    if answer == '1' or answer == 'лёгкая':
        await update.message.reply_text('Лёгкий уровень сложности:',
                                        reply_markup=ReplyKeyboardRemove())
        bot.send_photo(update.message.chat.id, photo=open('images/test_img.png', 'rb'),
                       caption='...answer...')
    if answer == '2' or answer == 'средняя':
        await update.message.reply_text('Средний уровень сложности:',
                                        reply_markup=ReplyKeyboardRemove())
        bot.send_photo(update.message.chat.id, photo=open('images/test_img.png', 'rb'),
                       caption='...answer...')
    if answer == '3' or answer == 'сложная':
        await update.message.reply_text('Сложный уровень сложности:',
                                        reply_markup=ReplyKeyboardRemove())
        bot.send_photo(update.message.chat.id, photo=open('images/test_img.png', 'rb'),
                       caption='...answer...')


async def create_profile_user(update, context):
    created_profile = cur.execute(f"""SELECT created_profile FROM statistics
                            WHERE id_users = {update.message.chat.id}""").fetchall()[0][0]
    if created_profile == 'no':
        user_id = update.message.from_user.id

        cur.execute(f"""UPDATE statistics SET created_profile = 'yes' WHERE id_users = {user_id}""")
        con.commit()

        date_created = str(datetime.now()).replace('.', ' ').split()[0:-1]
        date_created_profile = f"{date_created[0]} {date_created[1]}"
        cur.execute(f"""UPDATE statistics SET date_created_profile = '{date_created_profile}'
                    WHERE id_users = {user_id}""")
        con.commit()

        await update.message.reply_text('Ваш профиль создан\n'
                                        'Чтобы посмотреть его, напишите /profile')
    elif created_profile == 'yes':
        await update.message.reply_text('Вы уже создали свой профиль!\n'
                                        'Чтобы посмотреть его, напишите /profile')


async def view_profile(update, context):
    created_profile = cur.execute(f"""SELECT created_profile FROM statistics
                            WHERE id_users = {update.message.chat.id}""").fetchall()[0][0]

    if created_profile == 'yes':
        count_practice = cur.execute(f"""SELECT count_practice FROM statistics
                            WHERE id_users = {update.message.chat.id}""").fetchall()[0][0]
        count_theory = cur.execute(f"""SELECT count_theory FROM statistics
                            WHERE id_users = {update.message.chat.id}""").fetchall()[0][0]
        if count_practice != count_theory:
            if count_practice > count_theory:
                cur.execute(f"""UPDATE statistics SET favorite_activity = 'практика'
                            WHERE id_users = {update.message.chat.id}""")
            elif count_practice < count_theory:
                cur.execute(f"""UPDATE statistics SET favorite_activity = 'теория'
                            WHERE id_users = {update.message.chat.id}""")
            con.commit()

        user_photo = await telegram.Bot(token='6036045502:AAEN6Wb7h18Kfle3YDfropM7ZqIawZhH10c'). \
            getUserProfilePhotos(user_id=update.message.chat.id)
        user_photo = user_photo.photos[0][-1].file_id
        with Image.open('images/temp.jpg') as im:
            new_im = Image.new('RGB', (250, 250), (255, 255, 255))
            new_im.paste(im, (0, 0))
            user_photo_url = await bot_t.get_file(user_photo)
            user_photo_url = user_photo_url.file_path
            response = requests.get(user_photo_url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((250, 250))
            new_im.paste(img, (0, 0))
            new_im.save('images/profile.jpg')

        all_informations = cur.execute(f"""SELECT id_users, really_name,
                date_created_profile, favorite_activity
                 FROM statistics WHERE id_users = {update.message.chat.id}""").fetchall()[0]

        scores_all = cur.execute(f"""SELECT scores FROM statistics""").fetchall()
        scores_user = cur.execute(f"""SELECT scores FROM statistics
                                    WHERE id_users = {update.message.chat.id}""").fetchall()[0][0]
        p_scores = []
        for x in scores_all:
            p_scores.append(x[0])
        p_scores = sorted(p_scores, reverse=True)
        place_in_the_rating = p_scores.index(scores_user) + 1

        image_file = open('images/profile.jpg', 'rb')
        bot.send_photo(chat_id=update.message.chat_id,
                       photo=image_file,
                       caption=f"Имя: {all_informations[1]}\n"
                               f"ID: {all_informations[0]}\n"
                               f"Дата создания: {all_informations[2]}\n"
                               f"Любимая деятельность: {all_informations[3]}\n"
                               f"Баллы: {scores_user}\n"
                               f"Место среди других участников: {place_in_the_rating}")
        image_file.close()
    elif created_profile == 'no':
        await update.message.reply_text('Вы еще не создали профиль!\n'
                                        'Чтобы его создать, напишите /create_profile_user')


async def sdialog(update, context):
    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False,
                                 input_field_placeholder="скучаю по тебе!")
    await update.message.reply_text('Надеюсь ты узнал много нового!\n'
                                    'До скорых встреч!\n'
                                    'Возвращайся к нам через команду /start',
                                    reply_markup=markup)
    return ConversationHandler.END


def main():
    TOKEN = '6036045502:AAEN6Wb7h18Kfle3YDfropM7ZqIawZhH10c'
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'start_dialog': [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            'distribution': [MessageHandler(filters.TEXT & ~filters.COMMAND, distribution)],
            'distribution_fr': [MessageHandler(filters.TEXT & ~filters.COMMAND, distribution_fr)],
            'distribution_oge': [MessageHandler(filters.TEXT & ~filters.COMMAND, distribution_oge)],
            'check_answer': [MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer)],
            'distribution_ege': [MessageHandler(filters.TEXT & ~filters.COMMAND, distribution_ege)],
            'distribution_oge_or_ege': [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                       distribution_oge_or_ege)],
            'distribution_after_theory': [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                         distribution_after_theory)],
            'translate_text': [MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text)]
        },
        fallbacks=[CommandHandler('sdialog', sdialog)]
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('create_profile_user', create_profile_user))
    application.add_handler(CommandHandler('profile', view_profile))
    application.run_polling()


if __name__ == '__main__':
    main()
