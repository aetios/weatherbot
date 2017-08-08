#!/usr/bin/env python3

import requests


class StatusCodeException(Exception):
    pass


class API:
    def __init__(self, apikey):
        self.apikey = apikey
        self.success = None

    def get_weather(self, query):
        apiresp = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={self.apikey}")
        try:
            if apiresp.status_code != 200:
                raise StatusCodeException("status code not 200. Status code:", apiresp.status_code,
                                          "message:", apiresp.text)
            else:
                self.success = True
                return Weather(apiresp.json())
        except StatusCodeException:
            self.success = False

    def get_forecast(self, query):
        apiresp = requests.get(
            f"http://api.openweathermap.org/data/2.5/forecast?q={query}&appid={self.apikey}")
        try:
            if apiresp.status_code != 200:
                raise StatusCodeException("status code not 200. Status code:", apiresp.status_code,
                                          "message:", apiresp.text)
            else:
                self.success = True
                return Forecast(apiresp.json())
        except StatusCodeException:
            self.success = False

    def get_location(self, lat, lon):
        apiresp = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.apikey}")
        try:
            if apiresp.status_code != 200:
                raise StatusCodeException("status code not 200. Status code:", apiresp.status_code,
                                          "message:", apiresp.text)
            else:
                self.success = True
                return Weather(apiresp.json())
        except StatusCodeException:
            self.success = False


class Weather:
    def __init__(self, dr):
        weather = dr.get("weather")
        main = dr.get("main")
        wind = dr.get("wind")
        clouds = dr.get("clouds")
        rain = dr.get("rain")
        snow = dr.get("snow")
        sys = dr.get("sys")
        coord = dr.get("coord")

        if coord is not None:
            self.lon = coord.get("lon")
            self.lat = coord.get("lat")

        if weather is not None:
            self.w_type = []
            self.w_desc = []
            self.w_icon = []
            self.w_id = []

            for i in weather:
                self.w_type += [i.get("main")]  # concatenate self.w_type with 'i.get("main")' turned into a list
                self.w_desc += [i.get("description")]
                self.w_icon += [i.get("icon")]
                self.w_id += [i.get("id")]

        if main is not None:
            self.temp = main.get("temp")
            self.pressure = main.get("pressure")
            self.humidity = main.get("humidity")
            self.temp_min = main.get("temp_min")
            self.temp_max = main.get("temp_max")
            self.sea_level = main.get("sea_level")
            self.grnd_level = main.get("grnd_level")

        if wind is not None:
            self.windspeed = wind.get("speed")
            self.winddir = wind.get("deg")

        if clouds is not None:
            self.cloudiness = clouds.get("all")

        if rain is not None:
            self.rain = rain.get("3h")

        if snow is not None:
            self.snow = snow.get("3h")

        if sys is not None:
            self.cityid = sys.get("id")
            self.cityname = sys.get("name")
            self.sunrise = sys.get("sunrise")
            self.sunset = sys.get("sunset")

        self.visibility = dr.get("visibility")  # undocumented?


class Forecast:
    def __init__(self, dr):
        wlist = dr.get("list")  # weather list
        if wlist is not None:
            self.list = []
            for i in wlist:
                self.list += [Weather(i)]
                # print(i)

