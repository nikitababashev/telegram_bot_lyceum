import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


async def start(update, context):
    await update.message.reply_text('Привет! Как тебя зовут?')
    return 'start_dialog'


async def first_response(update, context):
    context.user_data['name'] = update.message.text
    if context.user_data['name'] == update.message.chat.first_name:
        await update.message.reply_text(f"Приятно познакомиться, {context.user_data['name']}!\n"
                                        f"Меня зовут Бот-Кеша.\n"
                                        f"Хочешь ли ты попробовать попрактиковаться в решение задач "
                                        f"из огэ или егэ по программированию?\n"
                                        f"Или же изначально ты хочешь прочитать теорию?\n"
                                        f"Чтобы выбрать, напиши: практика / теория")
        return 'distribution'
    else:
        await update.message.reply_text(f"Мне кажется, что ты хочешь меня обмануть!\n"
                                        f"Думаю, что тебя зовут {update.message.chat.first_name}"
                                        f", а не {context.user_data['name']}!\n"
                                        f"Верно?")
        return 'distribution_fr'


async def distribution_fr(update, context):
    answer = update.message.text
    if answer == 'да' or answer == 'верно':
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
                                        f"Чтобы выбрать, напиши: практика / теория")
        return 'distribution'
    elif answer == 'нет' or answer == 'не верно':
        await update.message.reply_text(f"Прошу прощения, мы - боты, еще не до конца развиты!\n"
                                        f"Приятно познакомиться, {context.user_data['name']}!\n"
                                        f"Меня зовут Бот-Кеша.\n"
                                        f"Хочешь ли ты попробовать попрактиковаться в решение задач "
                                        f"из огэ или егэ по программированию?\n"
                                        f"Или же изначально ты хочешь прочитать теорию?\n"
                                        f"Чтобы выбрать, напиши: практика / теория")
        return 'distribution'
    else:
        await update.message.reply_text(f"Извини, но я тебя не понимаю.\n"
                                        f"Ответь, пожалуйста, в формате: да / нет")
        return 'distribution_fr'


async def distribution(update, context):
    answer = update.message.text
    if answer == 'практика':
        reply_keyboard = [['ОГЭ', 'ЕГЭ']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False,
                                     input_field_placeholder="любим гусей")
        await update.message.reply_text('Хорошо, вижу, что ты уверен(а) в своих силах!\n'
                                        'Выбери из какого экзамена ты хочешь порешать задачи.',
                                        reply_markup=markup)
    return 'distribution_oge_or_ege'


async def distribution_oge_or_ege(update, context):
    answer = update.message.text
    if answer == 'ОГЭ':
        await update.message.reply_text('Вы выбрали - ОГЭ!\n'
                                        'Выберите сложность:\n'
                                        '1) лёгкая\n'
                                        '2) средняя\n'
                                        '3) сложная', reply_markup=ReplyKeyboardRemove())
        return 'distribution_oge'
    elif answer == 'ЕГЭ':
        return 'distribution_ege'


async def distribution_oge(update, context):
    answer = update.message.text
    if answer == '1' or answer == 'лёгкая':
        await update.message.reply_text('Лёгкий уровень сложности:')
        pass
    if answer == '2' or answer == 'средняя':
        await update.message.reply_text('Средний уровень сложности:')
        pass
    if answer == '3' or answer == 'сложная':
        await update.message.reply_text('Сложный уровень сложности:')
        pass


async def skip(update, context):
    await update.message.reply_text('Какая погода у вас за окном?')
    return 2


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
            'distribution_oge_or_ege': [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                       distribution_oge_or_ege)]
        },
        fallbacks=[CommandHandler('skip', skip)]
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
