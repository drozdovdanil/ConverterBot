import telebot
from utils import Converter, ConvertionExeption
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Отправьте сообщение боту в формате: \n<имя валюты> <имя валюты ' \
           '(в которую хотите перевести)> <количество первой валюты> ' \
            '\n\nПример: рубль доллар 300' \
            '\n\nЧто бы увидеть список доступных валют введите /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values_ = message.text.lower().split()

        if len(values_) != 3:
            raise ConvertionExeption('Проверьте параметры.\n<имя валюты> <имя валюты(в которую хотите перевести)> '
                                     '<количество первой валюты> ')

        quote, base, amount = values_
        amount = amount.replace(',', '.')
        total_base = Converter.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {quote} в {base} - {round(float(total_base) * float(amount), 2)}'
        bot.send_message(message.chat.id, text)


bot.polling()
