import os
import random
from flask import Flask, request
from pymessenger.bot import Bot
import json


 


app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']



bot = Bot(ACCESS_TOKEN)

#Получать сообщения, посылаемые фейсбуком нашему боту мы будем в этом терминале вызова
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
    # до того как позволить людям отправлять что-либо боту, Facebook проверяет токен,
    # подтверждающий, что все запросы, получаемые ботом, приходят из Facebook
        token_sent = request.args['hub.verify_token']
        return verify_fb_token(token_sent)
    # если запрос не был GET, это был POST-запрос и мы обрабатываем запрос пользователя
    else:
        # получаем сообщение, отправленное пользователем для бота в Facebook
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                #определяем ID, чтобы знать куда отправлять ответ
                    recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    text = message['message'].get('text').lower()
                    if 'цена' in text:
                        send_message(recipient_id, 'Какой город вас интересует?')
                    
                #если пользователь отправил GIF, фото, видео и любой не текстовый объект
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
        return "Message Processed"

def verify_fb_token(token_sent):
    '''Сверяет токен, отправленный фейсбуком, с имеющимся у вас.
    При соответствии позволяет осуществить запрос, в обратном случае выдает ошибку.'''
    if token_sent == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return 'Invalid verification token'

def send_message(recipient_id, response):
    '''Отправляет пользователю текстовое сообщение в соответствии с параметром response.'''
    bot.send_text_message(recipient_id, response)
    return 'Success'

def get_message():
    '''Отправляет случайные сообщения пользователю.'''
    sample_responses = ["Потрясающе!", "Я вами горжусь!", "Продолжайте в том же духе!", "Лучшее, что я когда-либо видел!"]
    return random.choice(sample_responses)

def menu():
    with open("persistent_menu.json", "r") as read_file:
        global data
        data = json.load(read_file)
    return bot.set_persistent_menu(data)

if __name__ == '__main__':
    app.run()