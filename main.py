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
    context.user_data['name'] = name = update.message.text
    await update.message.reply_text(f"Приятно познакомиться, {context.user_data['name']}!\n"
                                    f"Меня зовут Бот-Кеша.\n"
                                    f"Хочешь ли ты попробовать попрактиковаться в решение задач "
                                    f"из огэ или егэ по программированию?\n"
                                    f"Или же изначально ты хочешь прочитать теорию?\n"
                                    f"Чтобы выбрать, напиши практика/теория")
    return 'distribution'


async def distribution(update, context):
    answer = update.message.text
    if answer == 'практика':
        reply_keyboard = [['/oge', '/ege']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text('Хорошо, вижу, что ты уверен(а) в своих силах!\n'
                                        'Выбери из какого экзамена ты хочешь порешать задачи.',
                                        reply_markup=markup)


async def oge(update, context):
    print('огэ')


async def ege(update, context):
    print('егэ')


async def skip(update, context):
    await update.message.reply_text('Какая погода у вас за окном?')
    return 2


def main():
    TOKEN = '6036045502:AAEN6Wb7h18Kfle3YDfropM7ZqIawZhH10c'
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('oge', oge))
    application.add_handler(CommandHandler('ege', ege))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'start_dialog': [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            'distribution': [MessageHandler(filters.TEXT & ~filters.COMMAND, distribution)]
        },
        fallbacks=[CommandHandler('skip', skip)]
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
