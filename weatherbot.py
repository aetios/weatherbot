#!/usr/bin/env python3

import getweather
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import logging


weatherapi = getweather.API('6fa45a2cb67178aa918ad0544e3a73b6')
updater = Updater(token='404688712:AAFcRhLqpXURcuftyXmGdf_jqIN38_de0to')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    print(update.message.text)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello, this bot can give you the weather. Just invoke it by "
                          "typing /weather <searchterm>, this will return the current weather.\n "
                          "For best results, add a country name or code.\n"
                          "You can also use ZIP or postal codes in combination with a country.\n "
                          "You can also send a location.")


def gen_w_string(currentweather):
    w_string = ""
    for j, i in enumerate(currentweather.w_desc):
        if j > 0:
            w_string += ", "
        w_string += i
    return w_string.capitalize()


def response_1day(bot, update, query, currentweather):
    w_string = gen_w_string(currentweather)
    w_temp = str(round(currentweather.temp - 273.15, 1))

    bot.send_message(chat_id=update.message.chat_id,
                     text=f"*Weather for {query}:* \n{w_string}\nTemperature: {w_temp}°C", parse_mode="markdown")


def getweather(bot, update):
    query = update.message.text[9:]

    response_1day(bot, update, query.capitalize(), weatherapi.get_weather(query))


def location(bot, update):
    lon = update.message.location["longitude"]
    lat = update.message.location["latitude"]

    response_1day(bot, update, f"{lon}, {lat}", weatherapi.get_location(lat, lon))


start_handler = CommandHandler("start", start)
weather_handler = CommandHandler("weather", getweather)
location_handler = MessageHandler(Filters.location, location)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(weather_handler)
dispatcher.add_handler(location_handler)

updater.start_polling()
