import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import sqlite3
import telebot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)
con = sqlite3.connect('user_stat.db')
cur = con.cursor()
check_registration_users = []

bot = telebot.TeleBot('6036045502:AAEN6Wb7h18Kfle3YDfropM7ZqIawZhH10c')


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
                                        f"*не забывай, что ты можешь остановить"
                                        f" бота в любое время с помощью команды - /sdialog*",
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
        await update.message.reply_text(f"Приятно познакомиться, {context.user_data['name']}!\n"
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
        await update.message.reply_text(f"Мы - боты, развитые объекты, нас не так-то просто "
                                        f"обмануть!\n"
                                        f"Приятно познакомиться,"
                                        f" {context.user_data['name']}!\n"
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
        await update.message.reply_text(f"Прошу прощения, мы - боты, еще не до конца развиты!\n"
                                        f"Приятно познакомиться, {context.user_data['name']}!\n"
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
    if update.message.chat.id not in check_registration_users:
        cur.execute(f"""INSERT INTO statistics(id_users, really_name)
                        VALUES({context.user_data['id_user']}, '{context.user_data['name']}')""")
        con.commit()
    if answer == 'практика':
        reply_keyboard = [['ОГЭ', 'ЕГЭ']]
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
        await update.message.reply_text(f"Теория не менее важна, чем практика!\n"
                                        f"Ознакомиться с теорией можешь на нашем сайте:\n"
                                        f"      https://lyceum.yandex.ru/courses/766/groups/5718")


async def distribution_oge_or_ege(update, context):
    answer = update.message.text
    reply_keyboard = [['лёгкая', 'средняя', 'сложная']]
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
    answer = update.message.text.lower()
    if answer == '1' or answer == 'лёгкая':
        await update.message.reply_text('Лёгкий уровень сложности:',
                                        reply_markup=ReplyKeyboardRemove())
        print(1)
        bot.send_photo(update.message.chat.id, photo=open('test_img.png', 'rb'),
                       caption='...answer...')
    if answer == '2' or answer == 'средняя':
        await update.message.reply_text('Средний уровень сложности:',
                                        reply_markup=ReplyKeyboardRemove())
        bot.send_photo(update.message.chat.id, photo=open('test_img.png', 'rb'),
                       caption='...answer...')
    if answer == '3' or answer == 'сложная':
        await update.message.reply_text('Сложный уровень сложности:',
                                        reply_markup=ReplyKeyboardRemove())
        bot.send_photo(update.message.chat.id, photo=open('test_img.png', 'rb'),
                       caption='...answer...')


async def distribution_ege(update, context):
    answer = update.message.text.lower()
    if answer == '1' or answer == 'лёгкая':
        await update.message.reply_text('Лёгкий уровень сложности:',
                                        reply_markup=ReplyKeyboardRemove())
        bot.send_photo(update.message.chat.id, photo=open('test_img.png', 'rb'),
                       caption='...answer...')
    if answer == '2' or answer == 'средняя':
        await update.message.reply_text('Средний уровень сложности:',
                                        reply_markup=ReplyKeyboardRemove())
        bot.send_photo(update.message.chat.id, photo=open('test_img.png', 'rb'),
                       caption='...answer...')
    if answer == '3' or answer == 'сложная':
        await update.message.reply_text('Сложный уровень сложности:',
                                        reply_markup=ReplyKeyboardRemove())
        bot.send_photo(update.message.chat.id, photo=open('test_img.png', 'rb'),
                       caption='...answer...')


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
            'distribution_ege': [MessageHandler(filters.TEXT & ~filters.COMMAND, distribution_ege)],
            'distribution_oge_or_ege': [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                       distribution_oge_or_ege)]
        },
        fallbacks=[CommandHandler('sdialog', sdialog)]
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()