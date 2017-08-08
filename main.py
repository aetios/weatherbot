#!/usr/bin/env python3
#
import getweather
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import logging


weatherapi = getweather.API('')
updater = Updater(token='')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    print(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text="Hello, this bot can give you the weather. Just invoke it by "
                                                          "typing /weather <searchterm>, "
                                                          "this will return the current weather. Other functionality is"
                                                          " currently being added. \n"
                                                          "For best results, add a country name or code.\n"
                                                          "You can also use ZIP or postal codes in combination with a "
                                                          "country.\n You can also send a location.")


# def send_curweather(w_desc, w_temp):
#    pass


def genw_string(cur_weather):
    w_string = ""
    for j, i in enumerate(cur_weather.w_desc):
        if j > 0:
            w_string += ", "
        w_string += i
    return w_string


def getweather(bot, update):
    query = update.message.text[9:]

    currentweather = weatherapi.get_weather(query)

    w_string = genw_string(currentweather)
    w_temp = currentweather.temp - 273.15

    bot.send_message(chat_id=update.message.chat_id, text="*Weather for " + f"{query}".capitalize() + ":* \n" +
                     w_string.capitalize() + "\n" + "Temperature: " + str(round(w_temp, 1)) + "°C",
                     parse_mode="Markdown")


def location(bot, update):
    lon = update.message.location["longitude"]
    lat = update.message.location["latitude"]

    currentweather = weatherapi.get_location(lat, lon)

    w_string = genw_string(currentweather)
    w_temp = str(round(currentweather.temp - 273.15, 1))

    bot.send_message(chat_id=update.message.chat_id, text="*Weather for " + f"{lon}, {lat}" + ":* \n" +
                     w_string.capitalize() + "\n" + "Temperature: " + w_temp + "°C",
                     parse_mode="Markdown")


start_handler = CommandHandler("start", start)
weather_handler = CommandHandler("weather", getweather)
location_handler = MessageHandler(Filters.location, location)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(weather_handler)
dispatcher.add_handler(location_handler)

updater.start_polling()

