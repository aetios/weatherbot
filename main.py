#!/usr/bin/env python3
#
import getweather
from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging


weatherapi = getweather.API('')

updater = Updater(token='')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    print(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text="Hello, this bot can give you the weather. Just invoke it by "
                                                          "typing /weather [city] [countrycode], "
                                                          "this will return the current weather. Other functionality is"
                                                          " currently being added.")


def getweather(bot, update, args):
    print(update.message.text)

    for j, i in enumerate(args): print(j, ": ", i)

    currentweather = weatherapi.get_weather(args[0], args[1])
    print(currentweather)

    w_string = ""
    for j, i in enumerate(currentweather.w_type):
        if j > 0:
            w_string += ", "
        w_string += i

    print(currentweather.cityname)
    print(currentweather.cityid)
    print(currentweather.lon, currentweather.lat)

    bot.send_message(chat_id=update.message.chat_id, text="*Weather:* \n" +
                     w_string, parse_mode="Markdown")


start_handler = CommandHandler("start", start)
weather_handler = CommandHandler("weather", getweather, pass_args=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(weather_handler)

updater.start_polling()

