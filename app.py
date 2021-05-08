import telebot as tb
import time as t
from config import keys, TOKEN
from extensions import APIException, CryptoConvertor


bot = tb.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_handle(message: tb.types.Message):
    t.sleep(0.25)
    text = 'Это бот по конвертачии валюты.\nПолную инструкцию можно посмотреть.: /help'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help_handle(message: tb.types.Message):
    t.sleep(0.25)
    text = 'Чтобы начать работу дайте команду боту виде: \n'+''\
    '<Имя валюты> <Имя валюты в которую хотите перевести> <Кол-во первой валюты>. Вот пример "Доллар Евро 1"\n'+''\
    'Валюты нужно писать все с большой буквы, чтобы узнать курс обмена, нажмите /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values_handle(message: tb.types.Message):
    t.sleep(0.25)
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message: tb.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много или мало параметров.')
        quote, base, amount = values
        total_base = CryptoConvertor.get_price(quote, base, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалсь обработать команду.\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)