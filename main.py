#!/usr/bin/env python3

from getweather import *

api = API('6fa45a2cb67178aa918ad0544e3a73b6')
forecast = api.get_forecast('Holon', 'il')

# if api.success is True:
#     print(weather.temp)
#     print(weather.w_type)
# else:
#     print("Service Unavailable")
