#!/usr/bin/env python3
#
import getweather
from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging


weatherapi = getweather.API('')

updater = Updater(token='')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def start(bot, update):
    print(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text="Hello, this bot can give you the weather. Just invoke it by "
                                                          "typing /weather <searchterm>, "
                                                          "this will return the current weather. Other functionality is"
                                                          " currently being added. \n"
                                                          "For best results, add a country name or code.\n"
                                                          "You can also use ZIP or postal codes in combination with a "
                                                          "country.")


def getweather(bot, update):
    print(update.message.from_user)

    query = update.message.text[9:]
    print(query)

    currentweather = weatherapi.get_weather(query)
    print(currentweather)
    print(currentweather.w_type)

    w_string = ""
    for j, i in enumerate(currentweather.w_desc):
        if j > 0:
            w_string += ", "
        w_string += i

    w_temp = currentweather.temp - 273.15

    print(currentweather.cityname)
    print(currentweather.cityid)
    print(currentweather.lat, currentweather.lon)
    print(w_string)

    bot.send_message(chat_id=update.message.chat_id, text="*Weather for " + f"{query}".capitalize() + ":* \n" +
                     w_string.capitalize() + "\n" + "Temperature: " + str(round(w_temp, 1)) + "°C", parse_mode="Markdown")


start_handler = CommandHandler("start", start)
weather_handler = CommandHandler("weather", getweather)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(weather_handler)

updater.start_polling()

