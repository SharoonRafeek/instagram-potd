from instabot import Bot
from os import environ
import os
import shutil
import requests
import datetime


NASA_API = "k8fzYgYip4fLYqmVn5IsHzP99afQeyX4ADGrpFze"
NASA_URL = "https://api.nasa.gov/planetary/apod?api_key="
USERNAME = "nasa.potd"
PASSWORD = "Catalystno.8181"
IMAGE = "image.png"
POSTED = False


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
    # checking whether config folder exists or not
    if os.path.exists(dir):
        try:
            # removing it so we can upload new image
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

        if hour == 21 and minute == 13 and POSTED == False:
            clean_up(IMAGE)

            bot = Bot()
            bot.login(username=USERNAME, password=PASSWORD)

            title = data_collection()
            upload_post(IMAGE, title)
            POSTED = True

        if hour == 20 and minute == 45:
            POSTED = False


if __name__ == '__main__':
    main()