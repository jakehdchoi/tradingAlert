# https://chatbotslife.com/full-tutorial-on-how-to-create-and-deploy-a-telegram-bot-using-python-69c6781a8c8f
import requests

from config import *


def sendMessage(msg):
    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
        my_token, chat_id, msg)
    r = requests.get(url)
