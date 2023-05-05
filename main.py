from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

weather_key = os.environ["WEATHER_KEY"]

def get_weather():
  url = "https://api.seniverse.com/v3/weather/daily.json?key=Sm5EQa8fMVXzsMxjw&location=beijing&language=zh-Hans&unit=c&start=-1&days=2"
  res = requests.get(url).json()
  weather = res['results'][0]['daily'][0]
  return weather['text_day'], weather['text_night'],math.floor(int(weather['high'])),math.floor(int(weather['low'])),math.floor(float(weather['precip'])),math.floor(int(weather['wind_scale'])),weather['wind_direction']
      
#   当前位置：{{city.DATA}} 
#   今日白天的天气是：{{weather_day.DATA}} 
#   今日夜晚的天气是：{{weather_night.DATA}} 
#   有{{precip.DATA}}%的概率会下雨 
  
#   最高气温：{{temperature_high.DATA}}℃ 
#   最低气温：{{temperature_low.DATA}}℃ 
#   会有{{wind_scale.DATA}}级的{{wind_direction.DATA}}风哦 
#   这是我们相遇的第{{love_days.DATA}}天 
#   距离你的下一个生日还有{{birthday_left.DATA}}天 
  
#   今日土味情话： {{words.DATA}}

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

# def get_words():
#   words = requests.get("https://api.shadiao.pro/chp")
#   if words.status_code != 200:
#     return "一想到你，我这张脸就泛起微笑"
#   return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather_day,weather_night, temperature_high,temperature_low,precip,wind_scale,wind_direction = get_weather()
data = {"city":{"value":city, "color":get_random_color()},
        "weather_day":{"value":weather_day, "color":get_random_color()},
        "weather_night":{"value":weather_night, "color":get_random_color()},
        "temperature_high":{"value":temperature_high, "color":get_random_color()},
        "temperature_low":{"value":temperature_low, "color":get_random_color()},
        "precip":{"value":precip, "color":get_random_color()},
        "wind_scale":{"value":wind_scale, "color":get_random_color()},
        "wind_direction":{"value":wind_direction, "color":get_random_color()},
        "love_days":{"value":get_count() + 1, "color":get_random_color()},
        "birthday_left":{"value":get_birthday() - 1, "color":get_random_color()},
#         "words":{"value":get_words(), "color":get_random_color()}}
# get_words()
res = wm.send_template(user_id, template_id, data)
print(res)
