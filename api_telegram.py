# https://chatbotslife.com/full-tutorial-on-how-to-create-and-deploy-a-telegram-bot-using-python-69c6781a8c8f
import requests

from config import *

# msg = 'this is test'
# chat_id = '-335553489'


def sendMessage(msg):
    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
        my_token, chat_id, msg)
    r = requests.get(url)


# sendMessage(msg)
