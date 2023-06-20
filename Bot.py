import telebot
from config import TOKEN, keys
from extensions import ConvertionException, ValueConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    textStart = 'Чтобы начать работу введите команду в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n\
Пример: биткоин доллар 1\n\
Нажмите /values для получения списка валют'
    bot.reply_to(message, f"Здравствуйте, {message.chat.username}")
    bot.reply_to(message, textStart)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров!')

        quote, base, amount = values
        total_base = ValueConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос\n{e}')
    else:
        price = float(total_base) * float(amount)
        text = f'Цена {amount} {quote} в {base} равна {price}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
