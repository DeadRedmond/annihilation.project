import os
import configparser

if 'DYNO' in os.environ:
    Heroku = True

    token = os.getenv("BOT_TOKEN")
    google_api_key = os.getenv("SEARCH_API")
    custom_search_engine = os.getenv("SEARCH_ENGINE")
else:
    Heroku = False
    
    #читаем конфиг
    config = configparser.ConfigParser()
    config.read("settings.ini")

    token=config["BOT"]["token"]
    google_api_key=config["BOT"]["search_api"]
    custom_search_engine=config["BOT"]["search_engine"]