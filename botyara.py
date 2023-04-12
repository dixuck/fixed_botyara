import telebot
from decouple import config
from telebot import types
from parse import news, wishnum, get_description


TOKEN = config('TOKEN')  # name: botyara_n2; https://t.me/pityhonnbot

bot = telebot.TeleBot(TOKEN)

is_digit = lambda x: x.isdigit() if x[:1]!='-' else x[1:].isdigit()

photo, decs ='',''


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("start")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Привет, я был создан для одной из самых бесполезных целей - находить первые 20(или сколько угодно, но makers захотели 20) новостей Кыргызстана из сайта кактус или фикус не помню уже. Нажми start и получишь новости =(", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text.lower() == 'start':

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton('Quit')
        markup.add(btn2)
        ans = 'Напиши номер новости ниже и я дам тебе ее описание или изображение 👇\n'
        for new in news:
            ans += f'{str(new[0])}: {new[1][0]}\n'
        bot.send_message(message.from_user.id, ans, reply_markup=markup)

    elif is_digit(message.text):
        if int(message.text) in (range(1, wishnum+1)):

            for num, result in dict(news).items():
                
                if num == int(message.text):
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = types.KeyboardButton("description")
                    btn2 = types.KeyboardButton("photo")
                    btn3 = types.KeyboardButton('back')
                    markup.add(btn1, btn2, btn3)
                    global photo, desc
                    photo = result[2]
                    desc = get_description(result[1])
                    bot.send_message(message.from_user.id, 'some title news you can see Description of this news and Photo', reply_markup=markup)
        else: bot.send_message(message.from_user.id, 'Новости с таким номером нет')

    elif message.text.lower() == 'description':
        bot.send_message(message.from_user.id, desc)

        
    elif message.text.lower() == 'photo':
        bot.send_message(message.from_user.id, photo)

    elif message.text.lower() == 'back':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Вы вернулись назад", reply_markup=markup)
        message = bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEIiYdkNQAB8R1rH5m60wFnvV1pPO7WvPUAArMVAAJ4T9hLKHniCOysywEvBA')

    elif message.text.lower() == 'quit':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("start")
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'До свидания', reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю')

bot.polling(none_stop=True, interval=0)