from instabot import Bot
from os import environ
import os
import shutil
import requests
import datetime
import time


NASA_API = environ['NASA_API']
NASA_URL = environ['NASA_URL']
USERNAME = environ['USERNAME']
PASSWORD = environ['PASSWORD']

IMAGE = "image.png"
POSTED = False

bot = Bot()
time.sleep(30)
bot.login(username=USERNAME, password=PASSWORD)
            

def data_collection():
    data_response = requests.get(NASA_URL + NASA_API)
    data = data_response.json()
    media_url = data["url"]
    media_response = requests.get(media_url)

    if data["media_type"] != "video":
        with open("imgs/" + IMAGE, "wb") as img:
            img.write(media_response.content)

    title = data["title"]
    tags = '#NASA #space #astronomy #stars #universe #cosmos #cosmology #astrophotography #blackhole #nature ' \
           '#photography #picoftheday #huble #sun #moon #mars #cosmic #rocket #spacex #isro #singularity #galaxy'
    full_title = title + '.\n' + ' \n' + ' \n' + ' \n' + ' \n' + tags

    return full_title


def clean_up(i):
    dir = "config"
    remove_me = "imgs\{}.REMOVE_ME".format(i)
    
    if os.path.exists(dir):
        try:
            shutil.rmtree(dir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    if os.path.exists(remove_me):
        src = os.path.realpath("imgs\{}".format(i))
        os.rename(remove_me, src)


def upload_post(i, caption):
    global bot

    bot.upload_photo("imgs/{}".format(i), caption=caption)


def main():
    global bot, POSTED

    while True:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute

        if hour == 22 and minute == 40 and POSTED == False:
            
        
            title = data_collection()
            upload_post(IMAGE, title)
            clean_up(IMAGE)
            POSTED = True


        if hour == 22 and minute == 41:
            POSTED = False


if __name__ == '__main__':
    main()
