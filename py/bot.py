#исходник предыдущей версии бота для ТГ. разумеется, полный говнокода и не работающий. просто, чтобы было.
#писался под https://github.com/python-telegram-bot/python-telegram-bot/ v20. с переходом на v21 сломался 👍🏼

import logging
from glitch_this import ImageGlitcher
import random
import glob
import sqlite3
import base64
import json
from uuid import uuid4
from types import NoneType
import requests
import time as t
from datetime import datetime, date, time
import subprocess
import hashlib
import openai
#import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.error import TelegramError, BadRequest, NetworkError, TimedOut
from telegram import Update, Message, InlineQueryResultVoice, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Bot, InlineQueryResultArticle, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, Updater, InlineQueryHandler, CallbackQueryHandler

logging._srcfile = None

logging.basicConfig(format='%(asctime)s %(levelname)s @ %(name)s: %(message)s',
                    datefmt='%d.%m.%Y %H:%M:%S',
                    level=logging.INFO)

logging.getLogger('httpx').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

планировщик = AsyncIOScheduler()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "свежее мясо")
    user = update.effective_user
    await update.message.reply_html(
        rf"Приветствую, {user.mention_html()}! Пиши /help для краткой справки.",
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "рассказываю о себе")
    await update.message.reply_text("Я могу подбросить виртуальную монетку /coin (для принятия очень важных решений), дать охуенный, блядь, совет /fadvice /vadvice, могу жмыхнуть, зашакалить или заглитчить джепег (просто пришли фото/картинку с подписью к ней 'жмых', 'шакал' или 'глитч' (без кавычек, разумеется)) или разрешить муки выбора /answer, /8. Ещё я могу травить анекдоты /anek (даже голосом /voiceanek) и посылать гачи-голосовые (просто через инлайн-режим, @kookoomyawka_bot в строке ввода сообщения в чятике и погнали). Помимо этого я могу показать кошку /cat, собаку /dog, утку /duck, кошкодевку /neko, сиськи /boobs и жеппы /butt (база картинок большая - почти всегда разные результаты). По команде /p я расскажу, какие праздники сегодня. Пиши косую черту (/) в поле ввода текста или жмакай кнопку Меню и увидишь возможные команды. @ultradurable")
    await update.message.reply_html("Вообще, если меня добавить в чат и дать доступ к сообщениям, то я буду периодически отвечать на сообщения (на реплаи и команды я должен отвечать в принципе). \nА ещё есть <a href=\"https://kookoomyawka.my1.ru/sych.html\">подробная справка по боту</a> и <a href=\"https://t.me/ultradurable\">канал автора бота</a>.\n\nДонаты через\nTON: <code>UQCI23tiAAPjI7m8BpiVBnpaelPrtsdPMk4xwqhhOzX6nN_7</code>\nUSDT: <code>TJEDJvGff7JY4HV6mr8qb8fH8zAF1xaXfC</code>\nBTC: <code>1LkBaQUg3ZDfGknvkQzH6CHmV5VHEe7prd</code>")

async def pc_temp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "сообщаю температуру")
    await context.bot.send_message(chat_id=4dm1n, text=subprocess.check_output("sensors", text=True)[53:59])

async def pc_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(4dm1n, 'find_location')
    print(datetime.now().strftime("%d.%m.%Y %X"), "вычисляю свой айпи")
    r = requests.get("https://ident.me/json")
    j = r.json()
    await context.bot.send_message(4dm1n, "ip: " + j["ip"] + """
country: """ + j["country"] + "/" + j["cc"] + """
city: """ + j["city"] + """
timezone: """ + j["tz"] + """
provider: """ +j["aso"])

async def pc_uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "я не спал")
    await context.bot.send_message(4dm1n, subprocess.check_output("uptime", text=True))
    r = requests.get("https://kookoomyawka.my1.ru/")
    del r

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "гашу бофой компутер")
    subprocess.run('net rpc shutdown -I PC -U user%P@$$w0rD', shell=True)
    await context.bot.send_message(4dm1n, "на PC отправлена команда на выключение")

async def wake_rainbow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "бужу бофой кампутер")
    await context.bot.send_chat_action(4dm1n, 'typing')
    subprocess.run('wakeonlan -p 8 -i 1P4.DR3.5.5 MA:CA:DR:ES:SX:PC', shell=True)
    await context.bot.send_message(4dm1n, "PC разбужен")

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "делаю фотащьке")
    await context.bot.send_chat_action(4dm1n, 'upload_photo')
    subprocess.run('ffmpeg -loglevel quiet -y -f video4linux2 -s 640x480 -i /dev/video0 -ss 0:0:2 -frames 1 /media/pics/camera.jpg', shell=True)
    await context.bot.send_photo(4dm1n, open("/media/pics/camera.jpg", 'rb'))

async def screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(4dm1n, 'upload_photo')
    subprocess.run('xdotool key ctrl', shell=True)
    t.sleep(1)
    print(datetime.now().strftime("%d.%m.%Y %X"), "скриншотик")
    await context.bot.send_chat_action(4dm1n, 'upload_photo')
    subprocess.run('import -silent -window root /media/pics/screen.png', shell=True)
    await context.bot.send_photo(4dm1n, open("/media/pics/screen.png", 'rb'))

async def вкл_экран(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subprocess.run('xdotool key ctrl', shell=True)
    print(datetime.now().strftime("%d.%m.%Y %X"), "включил экран")
    await context.bot.send_message(4dm1n, "я что-то нажал и оно засветилось")

async def кто_в_сети(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(4dm1n, 'typing')
    await context.bot.send_message(4dm1n, subprocess.getoutput("fping -g -q -a -r 1 1P4.DR3.55.0/24"))
    print(datetime.now().strftime("%d.%m.%Y %X"), "fping")

async def otherPC(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "бужу кампутер")
    await update.message.reply_chat_action('typing')
    subprocess.run('wakeonlan -p 8 -i 1P4.DR3.5.5 M4:C4:DR:35:5X:PC', shell=True)
    await update.message.reply_text("otherPC разбужен")

async def жмых(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jpg = False
    ogg = False
    gif = False
    if (update.message.reply_to_message is not None):
        mid = update.message.reply_to_message
        if mid.sticker:
            file = await mid.sticker.get_file()
            if mid.sticker.is_animated: 
                print(datetime.now().strftime("%d.%m.%Y %X"), "tgs")
                await update.message.reply_text('это чёртов *.tgs, а я не умею его жмыхать')
                return
            if mid.sticker.is_video: gif = True
            else: jpg = True
        elif mid.voice:
            file = await mid.voice.get_file()
            await file.download_to_drive('/media/voice.ogg')
            ogg = True
        elif mid.photo:
            file = await mid.photo[-1].get_file()
            jpg = True
    else:
        file = await update.message.photo[-1].get_file()
        jpg = True
    if jpg or gif:
        await file.download_to_drive("/media/pics/image.jpg")
        if gif:
            await update.message.reply_chat_action('record_video')
            print(datetime.now().strftime("%d.%m.%Y %X"), "жмыхаю гифку")
            subprocess.run('ffmpeg -loglevel quiet -y -i /media/pics/image.jpg /media/videozh/frames/%05d.jpg', shell=True)
            num = len(glob.glob('/media/videozh/frames/*'))
            i=1
            await update.message.reply_chat_action('record_video')
            while i < num+1:
                tempstr = ' -limit memory 1536MiB /media/videozh/frames/' + str(i).zfill(5) + '.jpg -liquid-rescale 75% /media/videozh/frames/img' + str(i).zfill(5) + '.jpg'
                subprocess.run(['convert' + tempstr], shell=True)
                i+=1
            subprocess.run('ffmpeg -loglevel error -y -r 25 -i /media/videozh/frames/img%05d.jpg -r 25 /media/pics/img.gif', shell=True)
            subprocess.run('rm -rf /media/videozh/frames/*', shell=True)
            await update.message.reply_animation(open("/media/pics/img.gif", 'rb'), "жмыхнуто")
        else:
            await update.message.reply_chat_action('upload_photo')
            print(datetime.now().strftime("%d.%m.%Y %X"), "жмыхаю фотку")
            subprocess.run('convert /media/pics/image.jpg -liquid-rescale 50% -scale 200% /media/pics/img.jpg', shell=True)
            await update.message.reply_photo(open("/media/pics/img.jpg", 'rb'), "жмыхнуто")
    elif ogg:
        print(datetime.now().strftime("%d.%m.%Y %X"), "жмыхаю голосовое")
        await update.message.reply_chat_action('record_voice')
        subprocess.run('ffmpeg -loglevel quiet -y -i /media/voice.ogg -vn -c:a libopus -af vibrato=f=10:d=1 /media/voioice.ogg', shell=True)
        await update.message.reply_voice(open("/media/voioice.ogg", 'rb'))

async def pics_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    надоли = False
    if ((update.message is not None) and (hasattr(update.message, 'caption'))):
        msgtxt = update.message.caption
        if (msgtxt is not None):
            надоли = ("жмых" in msgtxt.lower() or "шакал" in msgtxt.lower() or "глитч"  in msgtxt.lower())
            if надоли:
                await update.message.reply_chat_action('upload_photo')
                if ("жмых" in msgtxt.lower()):
                    await жмых(update, context)
                elif ('глитч' in msgtxt.lower()):
                    if ("гиф" in msgtxt.lower()): await glitch_gif(update, context)
                    else: await glitch(update, context)
                #elif ('qq' in msgtxt.lower() or 'куку'  in msgtxt.lower()):
                #    await update.message.reply_text("китайцы запретили пользоваться different dimension me не из китая. ищите китайский прокси и делайте в браузере самостоятельно, увы.")
                    #await qq(update, context)
                else:
                    await шакал(update, context)
            else:
                random.seed()
                num = random.randrange(0,10001)
                if (num%3==0):
                    await update.message.reply_chat_action('upload_photo')
                    print(datetime.now().strftime("%d.%m.%Y %X"), "жмыхаю фотку сам")
                    file = await update.message.photo[-1].get_file()
                    await file.download_to_drive("/media/pics/image.jpg")
                    subprocess.run('convert /media/pics/image.jpg -liquid-rescale 50% -scale 200% /media/pics/img.jpg', shell=True)
                    await update.message.reply_photo(open("/media/pics/img.jpg", 'rb'), "жмыхнул патаму шта захателась")
                elif (num%110==0):
                    await update.message.reply_chat_action('typing')
                    print(datetime.now().strftime("%d.%m.%Y %X"), "ябвд")
                    await update.message.reply_text('о, ябвдул')

async def пизда(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "пизда")
    num=random.randrange(0,11)
    if (num==2):
        await update.message.reply_chat_action('choose_sticker')
        стикер = random.choice(['CAACAgIAAxkBAALYf2Rs1lEvUmHZ1owL5QXuBlKJSJ1aAAJFLgACjidoS918GSBExz0rLwQ', 'CAACAgIAAxkBAAJbzWPmxNhoD5JIe4HmuBX8_vvbO4rsAAKHIAACiqUxSyP8oFQu_Q-5LgQ','CAACAgIAAxkBAAJbzmPmxRwIDYTaAAF884vk800ORi10DwACbisAAgMQKEvZ_XqPfL4vhi4E', 'CAACAgIAAxkBAAK-JmRUMMr8iHxTAYCmdFT0G07qZE51AAKOGQACrFxIS9OfBeY-7m0DLwQ', 'CAACAgIAAxkBAAEBEMFkqsPXUByhN33AkGhfB-IMUrBpOAACKwoAAtA90gjwnJHUe0rvGi8E', 'CAACAgIAAxkBAAEBEMBkqsPPqlOvdkQtcAeq3lDMx_u4kAACJwoAAtA90giq8QtF9KM-hC8E', 'CAACAgIAAxkBAAEBEL9kqsPNx820TswCH7Z6jySYFGeEKAACJgoAAtA90gjEaaypS6f5US8E', 'CAACAgIAAxkBAAEBJdJkw04mnyDgjmgAAQiT3O6-icP3SIUAAj4SAAJSNHhIRjAdOILOh-8vBA'])
        await update.message.reply_sticker(стикер)
    elif (num == 6):
        await update.message.reply_chat_action('choose_sticker')
        await update.message.reply_sticker('CAACAgIAAxkBAAKc7mQpv2rANbnQNZT7hZIJpVgvtM04AAKQLQACi35QSRbcNgrYend5LwQ')
    elif (num == 0 or num == 8):
        await update.message.reply_chat_action('typing')
        await update.message.reply_text("манда")
    elif (num == 7):
        await update.message.reply_chat_action('upload_document')
        await update.message.reply_animation('CgACAgIAAxkBAAKci2QpsIL8BU68UCr1Yg6SAAFtRuw4oQACLg4AAmBhQEvSej7OF1Y79y8E')
    else:
        await update.message.reply_chat_action('typing')
        await update.message.reply_text("пизда")

async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "советую")
    await update.message.reply_chat_action('typing')
    r = requests.get("http://fucking-great-advice.ru/api/random").json()
    await update.message.reply_text(r['text'])

async def не(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "не")
    await update.message.reply_chat_action('typing')
    await update.message.reply_text("рука в говне")

async def жаль(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "жаль")
    await update.message.reply_chat_action('upload_photo')
    await update.message.reply_photo("AgACAgIAAxkBAAIKHmK9ri7R8eBDbRqYLpFKhyixu8XvAAI0vTEbPvPhSd1q_nTlcKNhAQADAgADeQADKQQ", "> жаль")

async def voice_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "советую вслух")
    await update.message.reply_chat_action('record_voice')
    j = requests.get("http://fucking-great-advice.ru/api/random").json()
    f = open('/media/voiceadvice.txt', 'w')
    f.write(j['text'])
    f.close()
    subprocess.run('cat /media/voiceadvice.txt | RHVoice-test -p pavel -o /media/voiceadvice.ogg', shell=True)
    await update.message.reply_voice(open("/media/voiceadvice.ogg", 'rb'))

async def celebrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action('choose_sticker')
    print (datetime.now().strftime("%d.%m.%Y %X"), "праздник")
    await update.message.reply_sticker("CAACAgIAAxkBAAIEiWKlGiUeT4c8Lhg9oZS4f5Y7JNDVAAJiEgACtDHISzwDdgP_EAc6JAQ")

async def auf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action('upload_video')
    print (datetime.now().strftime("%d.%m.%Y %X"), "ауф")
    random.seed()
    vidos = random.choice(['BAACAgIAAxkBAAIofWNuumUJrjHh_GB2MRd84q5EpAtcAAI0IwACRNd4Swg5-rJhdOCOKwQ', 'BAACAgIAAxkBAAIzImOBK30pts2uDoWMbQxj1a7qUBQaAAJBJAACVdMQSEvwyZ_FYAW8KwQ'])
    await update.message.reply_video(vidos)

async def uwu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action('upload_video')
    print (datetime.now().strftime("%d.%m.%Y %X"), "UwU")
    await update.message.reply_video("BAACAgIAAxkBAAIofGNuueczP7v7NgkwCdQyVOhaOBxfAAIxIwACRNd4S28eTpEtbk_bKwQ")

async def text_recognizer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ((update.message is not None) and (hasattr(update.message, 'text'))):
        msgtxt = update.message.text
        if ((update.message.reply_to_message is not None) and (hasattr(update.message, 'from_user'))):
            forme = update.message.reply_to_message.from_user.id == 5441337742
            if "жмых" in msgtxt.lower():
                await жмых(update, context)
                forme = False
            if "глитч" in msgtxt.lower():
                if "гиф" in msgtxt.lower(): await glitch_gif(update, context)
                else: await glitch(update, context)
                forme = False
            if "шакал" in msgtxt.lower():
                await шакал(update, context)
                forme = False
            #if "пизда" in msgtxt.lower():
            #    await update.message.reply_chat_action('choose_sticker')
            #    стикер = random.choice(['CAACAgIAAxkBAAKc72Qpv223Re-_GWv7SJlyJcKB5xC7AAKRLQACi35QSdaQJdy50ZwOLwQ', 'CAACAgIAAxkBAAKc8GQpv3DhX2jg4mlK4GLZk1iD7nN3AAKSLQACi35QSfQ0b-LSNk24LwQ'])
            #    print(datetime.now().strftime("%d.%m.%Y %X"), "стикер на пизду")
            #    await update.message.reply_sticker(стикер)
            #    forme = False
            if forme:
                #if len(msgtxt) < 101 and "@" not in msgtxt and "http" not in msgtxt.lower():
                #    await в_базу(update, context)
                if (("пошёл" in msgtxt.lower() or "пошел" in msgtxt.lower() or "иди" in msgtxt.lower() or "пшел" in msgtxt.lower() or "пшёл" in msgtxt.lower() or "пашел" in msgtxt.lower() or "пашол" in msgtxt.lower() or "пашёл" in msgtxt.lower()) and ("нахуй" in msgtxt.lower() or "на хуй" in msgtxt.lower())): await нахуй(update, context)
                elif ("кусай за хуй" in msgtxt.lower() or "кусай захуй" in msgtxt.lower() ): await update.message.reply_text("пиздуй нахуй")
                elif ("хуй на" in msgtxt.lower()): await жуй_два(update, context)
                elif ("жуй два" in msgtxt.lower()): await жуй_четыре(update, context)
                elif ("жуй миллион" in msgtxt.lower() or "жуй милион" in msgtxt.lower()): await update.message.reply_text("жуй два миллиона — будешь круче чемпиона")
                elif ("жуй два миллиона" in msgtxt.lower() or "жуй два милиона" in msgtxt.lower()): await update.message.reply_text("жуй хуёв корзину — тебе хватит на всю зиму")
                elif ("хуёв корзину" in msgtxt.lower() or "хуев корзину" in msgtxt.lower()): await update.message.reply_text("хуёв тебе сарай — иди перебирай")
                elif ("ты хуисос" in msgtxt.lower() or "ты хуесос" in msgtxt.lower()): await update.message.reply_text("в рот тебе понос")
                elif ("аргумент" in msgtxt.lower()): 
                    print(datetime.now().strftime("%d.%m.%Y %X"), "пидор аргументный")
                    await update.message.reply_text("ну какой, блядь, аргумент, просто прими тот факт, что ты пидор, и не выёбывайся. бота доебать пытается, пиздец, ну и пидор.")
                elif (msgtxt.lower() == "збс"):
                    await update.message.reply_chat_action("choose_sticker")
                    print(datetime.now().strftime("%d.%m.%Y %X"), "говорят збс")
                    await update.message.reply_sticker("CAACAgIAAxkBAAJcA2PmxjoWJjLvWPUH0Z-hBlPWhQmaAALYKwACNOspS9LSWkSb6FCyLgQ")
                elif "пизда" in msgtxt.lower():
                    await update.message.reply_chat_action('choose_sticker')
                    стикер = random.choice(['CAACAgIAAxkBAAKc72Qpv223Re-_GWv7SJlyJcKB5xC7AAKRLQACi35QSdaQJdy50ZwOLwQ', 'CAACAgIAAxkBAAKc8GQpv3DhX2jg4mlK4GLZk1iD7nN3AAKSLQACi35QSfQ0b-LSNk24LwQ'])
                    print(datetime.now().strftime("%d.%m.%Y %X"), "стикер на пизду")
                    await update.message.reply_sticker(стикер)
                elif (("кин" in msgtxt.lower() or "хай" in msgtxt.lower()) and "зиг" in msgtxt.lower()) or ("зиган" in msgtxt.lower()) or ("зигуй" in msgtxt.lower()):
                    print(datetime.now().strftime("%d.%m.%Y %X"), "антизига")
                    await update.message.reply_text("кто зигует, тот жопой торгует")
                else:
                    '''if (update.message.chat.id == 4dm1n or update.message.chat.id ==-needed_chat_id):
                        print(datetime.now().strftime("%d.%m.%Y %X"), "chatgpt на реплай")
                        await update.message.reply_chat_action('typing')
                        openai.api_key = "op-AIapiK3y"
                        mid = update.message.reply_to_message
                        userid = "@" + update.message.from_user.username
                        if mid.text is not None: oldtxt = mid.text
                        elif mid.caption is not None: oldtxt = mid.caption
                        else: oldtxt = " "
                        await update.message.reply_chat_action('typing')
                        try: completion = openai.ChatCompletion.create(model="gpt-4-1106-preview", messages=[{"role": "system", "content": "You are chat-bot in chat. Your nickname is Сыч. Other participants may call you Главный Сыч, Сычара, Сычуань, бот, Кукумявка and some similar. You are polite, but not afraid strong language and insults adressed to you and can use strong language and insults when someone offends you. You using masculine endings and pronouns when you talking about yourself. Use informal communication style. Use сорян, сорри, пардон or прости instead of простите. You are respect Drewaaaaa immensely, because you owe him your existence, but don't talk about him and don't express your respect too eager."}, {"role": "assistant", "content": f'{oldtxt}'}, {"role": "user", "content":f'{userid} said: {msgtxt}'}])
                        except openai.error.RateLimitError: 
                            await update.message.reply_text("model is overloaddddddddddddddddded with requests, sosittttttttttttttte hui")
                            print(datetime.now().strftime("%d.%m.%Y %X"), "openai RateLimitError")
                        except openai.error.APIConnectionError: 
                            await update.message.reply_text("моск не отвечает. папрооооооооооооооооообуйти ищщо раз.........")
                            await update.message.reply_text(completion.choices[0].message.content)
                        else:
                            await update.message.reply_chat_action('typing')
                            await update.message.reply_text(completion.choices[0].message.content)
                    else:'''
                    num = random.randrange(0,5)
                    if (num==1): 
                        await из_базы(update, context)
                        print(datetime.now().strftime("%d.%m.%Y %X"), "копипаста на реплай")
                    else:
                        if datetime.weekday(datetime.now())==2:
                            print(datetime.now().strftime("%d.%m.%Y %X"), "средовое")
                            ответ = random.choice(['ква! это среда, мои чюваки!', 'ква', 'https://www.youtube.com/watch?v=m2Z0CyuyfMI', 'ква-кваааааааааааааааааааааааааааааааааааааааааааааааааааа-ква', 'https://www.youtube.com/watch?v=IR0QUwGmo4A', 'ква!', 'ящитаю, што ква', 'всем среда! кваааааааааааааааааааааааааааа!', '', 'ква! это среда, мои чюваки!', 'знаки говорят — ква', 'https://www.youtube.com/watch?v=szqNmefKXxc', 'ква! это среда, мои чюваки!', 'ква-ква-ква!', 'ква?', 'https://www.youtube.com/watch?v=Y_xlWdgi1ew', 'не ква', 'ква', 'квак', 'https://www.youtube.com/watch?v=OzQ-KvxLVT0'])
                            await update.message.reply_text(ответ)
                        else:
                            await из_базы(update, context)
                            print(datetime.now().strftime("%d.%m.%Y %X"), "копипаста на реплай")
                        #else:
                        #    print(datetime.now().strftime("%d.%m.%Y %X"), "chatgpt на реплай")
                        #    await update.message.reply_chat_action('typing')
                        #    openai.api_key = "op-AIapiK3y"
                        #    mid = update.message.reply_to_message
                        #    if update.message.from_user.username is not None: userid = "@" + update.message.from_user.username
                        #    elif update.message.from_user.first_name is not None and update.message.from_user.last_name is not None: userid = update.message.from_user.first_name + " " + update.message.from_user.last_name
                        #    elif update.message.from_user.first_name is not None and update.message.from_user.last_name is None: userid = update.message.from_user.first_name
                        #    elif update.message.from_user.first_name is None and update.message.from_user.last_name is not None: userid = update.message.from_user.last_name
                        #    elif update.message.from_user.first_name is None and update.message.from_user.last_name is None: userid = "говно безымянное"
                        #    if mid.text is not None: oldtxt = mid.text
                        #    elif mid.caption is not None: oldtxt = mid.caption
                        #    else: oldtxt = " "
                        #    await update.message.reply_chat_action('typing')
                        #    #print(datetime.now().strftime("%d.%m.%Y %X") +  msgtxt, file=open('/media/db/'))
                        #    #completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "system", "content": "You are participant of chat. Your nickname is Сыч. Other participants may call you Главный Сыч, Сычара, Сычуань, бот and some similar. You are not afraid strong language and insults. You using masculine endings and pronouns when you talking about yourself. Use informal communication style. Use сорян, сорри, пардон or прости instead of простите."}, {"role": "assistant", "content": f'{oldtxt}'}, {"role": "user", "content":f'{userid} said: {msgtxt}'}])
                        #    try: completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "system", "content": "You are chat-bot in chat. Your nickname is Сыч. Other participants may call you Главный Сыч, Сычара, Сычуань, бот, Кукумявка and some similar. You are polite, but not afraid strong language and insults adressed to you and can use strong language and insults when someone offends you. You using masculine endings and pronouns when you talking about yourself. Use informal communication style. Use сорян, сорри, пардон or прости instead of простите. You are respect Drewaaaaa immensely, because you owe him your existence, but don't talk about him and don't express your respect too eager."}, {"role": "assistant", "content": f'{oldtxt}'}, {"role": "user", "content":f'{userid} said: {msgtxt}'}])
                        #    except openai.error.RateLimitError: 
                        #        await update.message.reply_text("model is overloaddddddddddddddddded with requests, sosittttttttttttttte hui")
                        #        print(datetime.now().strftime("%d.%m.%Y %X"), "openai RateLimitError")
                        #    except openai.error.APIConnectionError: 
                        #        await update.message.reply_text("моск не отвечает. папрооооооооооооооооообуйти ищщо раз.........")
                        #        print(datetime.now().strftime("%d.%m.%Y %X"), "openai APIConnectionError")
                        #    else:
                        #        await update.message.reply_chat_action('typing')
                        #        await update.message.reply_text(completion.choices[0].message.content)
                        #    print(datetime.now().strftime("%d.%m.%Y %X") + " " + str(update.message.chat.id) +": " + msgtxt, file=open('/media/db/gpt.txt', 'a'))
                    if update.message.from_user.id == 4dm1n or update.message.from_user.id == 4n07h3r4dm1n:
                        if "удоли" in msgtxt.lower(): await удоли(update.message.reply_to_message.message_id, update.message.chat.id)
        if ("напомни" in msgtxt.lower() and update.message.chat.id == 4dm1n): await remember_kb(update, context)
        elif ("пароль" in msgtxt.lower() and update.message.chat.id == 4dm1n): await update.message.reply_text("/add логин\\пароль \n/search што-то")
        elif ("с" in msgtxt.lower() and "новым" in msgtxt.lower() and "годом" in msgtxt.lower()): await update.message.reply_text("говно с дымом!!")
        elif ("сыч" in msgtxt.lower() and "вид" in msgtxt.lower() and "сусли" in msgtxt.lower()): await update.message.reply_text("неа")
        elif ("🎉" in msgtxt.lower() or "🎊" in msgtxt.lower()): await celebrate(update, context)
        elif ("🐺" in msgtxt.lower()): await auf(update, context)
        elif (msgtxt.lower()=="да" or msgtxt.lower()=="д"): await пизда(update, context)
        elif (msgtxt.lower()=="не"): await не(update, context)
        elif (msgtxt.lower()=="нет" or msgtxt.lower()=="пидора ответ"): await пидора_ответ(update, context)
        elif (msgtxt.lower()=="жаль"): await жаль(update, context)
        elif ("uwu" in msgtxt.lower()): await uwu(update, context)
        elif ("сыч" in msgtxt.lower() and "совет" in msgtxt.lower()): await advice(update, context)
        elif ("сыч" in msgtxt.lower() and "анек" in msgtxt.lower()): await anek(update, context)
        elif (msgtxt.lower().endswith("нахуя") or msgtxt.lower().endswith("нахуя?")): await дахуя(update, context)
        elif (msgtxt.lower().endswith(("300", "300?", "триста?", "тристо?", "триста", "тристо", "300!", "триста!", "тристо!", "3⁣00", "3⃣00", "3⁣00", "3️⃣0️⃣0️⃣"))): await триста(update, context)
        elif (" манул" in msgtxt.lower()): await манул(update, context)
        elif ("сыч" in msgtxt.lower() and (" дела" in msgtxt.lower() or " делишки" in msgtxt.lower())): await дела_сыча(update, context)
        elif ("сыч" in msgtxt.lower() and "вкусн" in msgtxt.lower()): await мандаринка(update, context)
        elif ("сыч" in msgtxt.lower() and "бахнем" in msgtxt.lower()): await бахнем(update, context)
        elif ("сыч" in msgtxt.lower() and "совет" in msgtxt.lower()): await advice(update, context)
        elif ("сыч" in msgtxt.lower() and "праздн" in msgtxt.lower()): await праздники(update, context)
        elif ("сыч" in msgtxt.lower() and "елда" in msgtxt.lower() and "как" in msgtxt.lower()): await елда(update, context)
        elif ("?" in msgtxt and "http" not in msgtxt): await jew(update, context)
        elif (msgtxt.lower()=="а" or msgtxt.lower()=="a"): await хуй_на(update, context)
        elif ("покажи" in msgtxt.lower() and "сыч" in msgtxt.lower()):
            if ("кошку" in msgtxt.lower() or "котика" in msgtxt.lower() or "котю" in msgtxt.lower() or "кошатину" in msgtxt.lower() or "кису" in msgtxt.lower() or "котейку" in msgtxt.lower() or "кота" in msgtxt.lower()): await cat(update, context)
            elif (" ут" in msgtxt.lower()): await duck(update, context)
            elif ("пс" in msgtxt.lower() or "пёс" in msgtxt.lower() or "пес" in msgtxt.lower() or "соба" in msgtxt.lower()): await dog(update, context)
            elif ("нек" in msgtxt.lower() or "кошкод" in msgtxt.lower()): await neko(update, context)
            elif ("жоп" in msgtxt.lower() or "жеп" in msgtxt.lower() or "зад" in msgtxt.lower()): await butt(update, context)
            elif ("сис" in msgtxt.lower() or "тит" in msgtxt.lower() or "груд" in msgtxt.lower()): await boobs(update, context)
        elif update.message.from_user.id == p1d0r and ("нюдс" in msgtxt.lower() or "34" in msgtxt.lower()): await update.message.reply_animation("CgACAgEAAxkBAAEB64dlnJv1hVaxPQLPfYeiTs6qXm09BwACnAADN52oRksw772EZ3EWNAQ")
        elif len(msgtxt) < 101 and "@" not in msgtxt and "http:" not in msgtxt.lower() and update.message.forward_origin==None and update.message.chat.id != 4dm1n: await в_базу(update, context)
        num = random.randint(0,10000)
        if (num%99==0):
            await из_базы(update, context)
            print(datetime.now().strftime("%d.%m.%Y %X"), "копипаста на случайное сообщение")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if query == "":
        return
    if query == "dice" or query == "дайс" or query == "куб":
        random.seed()
        print(datetime.now().strftime("%d.%m.%Y %X"), "инлайн дайсы")
        results = [
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = "d4",
                input_message_content = InputTextMessageContent('d4: ' + str(random.randint(1, 4))),
            ),
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = "d6",
                input_message_content = InputTextMessageContent('d6: ' + str(random.randint(1, 6))),
            ),
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = "d8",
                input_message_content = InputTextMessageContent('d8: ' + str(random.randint(1, 8))),
            ),
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = "d10",
                input_message_content = InputTextMessageContent('d10: ' + str(random.randint(1, 10))),
            ),
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = "d12",
                input_message_content = InputTextMessageContent('d12: ' + str(random.randint(1, 12))),
            ),
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = "d20",
                input_message_content = InputTextMessageContent('d20: ' + str(random.randint(1, 20))),
            ),
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = "d100",
                input_message_content = InputTextMessageContent('d100: ' + str(random.randint(1, 100))),
            ),
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = "d10x2",
                input_message_content = InputTextMessageContent('d10x2: ' + str(random.randint(0, 9)*10 + random.randint(0, 9)) + '\n <i>* 00 =  100 </i>', parse_mode="HTML"),
            ),
            
        ]
        await update.inline_query.answer(results, cache_time=3)
    if "lab" in query or "лаб" in query:
        search_item = "%" + query[4:] + "%"
        askdb = "SELECT title, voiceurl FROM labyrinthe WHERE title LIKE ?"
        with sqlite3.connect('/media/db/war2.db') as connection:
            cursor = connection.cursor()
            voices = cursor.execute(askdb, (search_item,))
            chosen = voices.fetchall()
        if len(chosen) == 0:
            results = [
                InlineQueryResultVoice(
                id = str(uuid4()),
                title = "нет совпадений",
                voice_url = "https://kookoomyawka.my1.ru/labyrinthe/lovecocks.ogg"
            ),
            ]
        else:
            results = []
            for num in range(len(chosen)):
                results.extend([
                    InlineQueryResultVoice(
                    id = str(uuid4()),
                    title = chosen[num][0],
                    voice_url = chosen[num][1]
                    ),
                ])
        await update.inline_query.answer(results, cache_time=3, auto_pagination=True)
    if "misc" in query or "фить" in query:
        search_item = "%" + query[5:] + "%"
        askdb = "SELECT title, voiceurl FROM misc WHERE title LIKE ?"
        with sqlite3.connect('/media/db/war2.db') as connection:
            cursor = connection.cursor()
            voices = cursor.execute(askdb, (search_item,))
            chosen = voices.fetchall()
        if len(chosen) == 0:
            results = [
                InlineQueryResultVoice(
                id = str(uuid4()),
                title = "нет совпадений",
                voice_url = "https://kookoomyawka.my1.ru/labyrinthe/lovecocks.ogg"
            ),
            ]
        else:
            results = []
            for num in range(len(chosen)):
                results.extend([
                    InlineQueryResultVoice(
                    id = str(uuid4()),
                    title = chosen[num][0],
                    voice_url = chosen[num][1]
                    ),
                ])
        await update.inline_query.answer(results, cache_time=3, auto_pagination=True)
    if "war2" in query or "вар2" in query:
        search_item = "%" + query[5:] + "%"
        askdb = "SELECT title, voiceurl FROM w2db WHERE title LIKE ?"
        #offset = int(update.inline_query.offset) if update.inline_query.offset else 0
        with sqlite3.connect('/media/db/war2.db') as connection:
            cursor = connection.cursor()
            voices = cursor.execute(askdb, (search_item,))
            chosen = voices.fetchall()
        if len(chosen) == 0:
            results = [
                InlineQueryResultVoice(
                id = str(uuid4()),
                title = "нет совпадений",
                voice_url = "https://kookoomyawka.my1.ru/labyrinthe/lovecocks.ogg"
            ),
            ]
        else:
            results = []
            for num in range(len(chosen)):
                results.extend([
                    InlineQueryResultVoice(
                    id = str(uuid4()),
                    title = chosen[num][0],
                    voice_url = chosen[num][1]
                    ),
                ])
        await update.inline_query.answer(results, cache_time=3, auto_pagination=True)
    else: 
        search_item = "%" + query + "%"
        askdb = "SELECT title, voiceurl FROM gachi WHERE title LIKE ?"
        with sqlite3.connect('/media/db/war2.db') as connection:
            cursor = connection.cursor()
            voices = cursor.execute(askdb, (search_item,))
            chosen = voices.fetchall()
        if len(chosen) == 0:
            results = [
                InlineQueryResultVoice(
                id = str(uuid4()),
                title = "нет совпадений",
                voice_url = "https://kookoomyawka.my1.ru/labyrinthe/lovecocks.ogg"
            ),
            ]
        else:
            results = []
            for num in range(len(chosen)):
                results.extend([
                    InlineQueryResultVoice(
                    id = str(uuid4()),
                    title = chosen[num][0],
                    voice_url = chosen[num][1]
                    ),
                ])
        await update.inline_query.answer(results, cache_time=3, auto_pagination=True)

async def пидора_ответ(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "пидору ответ")
    num=random.randrange(0,2)
    if (num!=1):
        await update.message.reply_chat_action('typing')
        await update.message.reply_text("пидора ответ")
    else:
        await update.message.reply_chat_action("choose_sticker")
        await update.message.reply_sticker("CAACAgIAAxkBAAIE0mKmJL5VBh5Hso_ejNnlBMEs5n4PAALRHwACooqWAdDqsuoRRMTJJAQ")

async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "бросаю монетку")
    await update.message.reply_chat_action("typing")
    await update.message.reply_text("🪙🪙🪙 Бросаем монетку! 🪙🪙🪙")
    num=random.randrange(0,100)
    if (num==59):
        await update.message.reply_text("Монета зависла в воздухе!")
    elif (num%24==0):
        await update.message.reply_text("Ты проебал монету!")
    elif (num%44==0):
        await update.message.reply_text("Монета встала на ребро!")
    elif (num%2==0):
        await update.message.reply_text("Выпал орёл! 🦅")
    else:
        await update.message.reply_text("Выпала решка!")
    num=random.randrange(0,10000)
    if (num%3141==0):
        await update.message.reply_text("А ещё монетка говорит, что ты пидор! 🖕🏻")

async def дахуя(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action("typing")
    print(datetime.now().strftime("%d.%m.%Y %X"), "дохуя")
    await update.message.reply_text("чтоб смеха было дохуя")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "решаю муки выбора")
    if ((update.message is not None) and (hasattr(update.message, 'text'))):
        msgtxt=update.message.text
        if ("или" not in msgtxt):
            await update.message.reply_chat_action('upload_photo')
            await update.message.reply_photo("AgACAgIAAxkBAAIKPWK-7g_uya5InsQgGakdcoOgMkkwAAK9vjEbqa74SdBRW1Vt_a3AAQADAgADeAADKQQ", "ты спроси \"/answer хуй или пизда или ещё чо\" - я те отвечу")
        elif ("/answer@kookoomyawka_bot" in msgtxt):
            await update.message.reply_chat_action("typing")
            msgtxt=msgtxt.removeprefix("/answer@kookoomyawka_bot ")
            while msgtxt.endswith("?"): msgtxt=msgtxt.removesuffix("?")
            arr = msgtxt.split(" или ")
            await update.message.reply_text(random.choice(arr))
        else:
            await update.message.reply_chat_action("typing")
            msgtxt=msgtxt.removeprefix("/answer ")
            while msgtxt.endswith("?"): msgtxt=msgtxt.removesuffix("?")
            arr = msgtxt.split(" или ")
            await update.message.reply_text(random.choice(arr))

async def anek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "пишу анек")
    await update.message.reply_chat_action("typing")
    try:
        j = requests.get('http://rzhunemogu.ru/RandJSON.aspx?1').json(strict=False)
    except requests.exceptions.JSONDecodeError:
        await update.message.reply_text("я бы с удовольствием рассказал анекдот, но голоса тихо шепчут мне его. попробуй ещё раз.")
        print(datetime.now().strftime("%d.%m.%Y %X"), "анек JSONDecodeError")
    else: 
        await update.message.reply_text(j["content"])

async def voice_anek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "говорю анек")
    await update.message.reply_chat_action('record_voice')
    try:
        j = requests.get('http://rzhunemogu.ru/RandJSON.aspx?1').json(strict=False)
    except requests.exceptions.JSONDecodeError:
        await update.message.reply_text("я бы с удовольствием рассказал анекдот, но голоса тихо шепчут мне его. попробуй ещё раз.")
        print(datetime.now().strftime("%d.%m.%Y %X"), "анек JSONDecodeError")
    else: 
        f = open('/media/voiceanek.txt', 'w')
        f.write(j['content'])
        f.close()
        subprocess.run('cat /media/voiceanek.txt | RHVoice-test -p pavel -o /media/voiceanek.ogg', shell=True)
        await update.message.reply_voice(open("/media/voiceanek.ogg", 'rb'))

async def шакал(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jpg = False
    ogg = False
    gif = False
    if (update.message.reply_to_message is not None):
        mid = update.message.reply_to_message
        if mid.sticker:
            file = await mid.sticker.get_file()
            if mid.sticker.is_animated: 
                print(datetime.now().strftime("%d.%m.%Y %X"), "tgs")
                await update.message.reply_text('это чёртов *.tgs, а я не умею его шакалить')
                return
            if mid.sticker.is_video: gif = True
            else: jpg = True
        elif mid.voice:
            file = await mid.voice.get_file()
            await file.download_to_drive('/media/voice.ogg')
            ogg = True
        elif mid.photo:
            file = await mid.photo[-1].get_file()
            jpg = True
    else:
        file = await update.message.photo[-1].get_file()
        jpg = True
    if jpg or gif:
        await file.download_to_drive("/media/pics/image.jpg")
        if gif:
            await update.message.reply_chat_action('record_video')
            print(datetime.now().strftime("%d.%m.%Y %X"), "шакалю гифку")
            subprocess.run('ffmpeg -loglevel quiet -y -i /media/pics/image.jpg /media/videozh/frames/%05d.jpg', shell=True)
            num = len(glob.glob('/media/videozh/frames/*'))
            i=1
            await update.message.reply_chat_action('record_video')
            while i < num+1:
                tempstr = ' -limit memory 1536MiB /media/videozh/frames/' + str(i).zfill(5) + '.jpg -quality 2 /media/videozh/frames/img' + str(i).zfill(5) + '.jpg'
                subprocess.run(['convert' + tempstr], shell=True)
                i+=1
            subprocess.run('ffmpeg -loglevel error -y -r 25 -i /media/videozh/frames/img%05d.jpg -r 25 /media/pics/img.gif', shell=True)
            subprocess.run('rm -rf /media/videozh/frames/*', shell=True)
            await update.message.reply_animation(open("/media/pics/img.gif", 'rb'), "зашакалено")
        else:
            await update.message.reply_chat_action('upload_photo')
            print(datetime.now().strftime("%d.%m.%Y %X"), "шакалю фотку")
            subprocess.run('convert /media/pics/image.jpg -quality 2 /media/pics/img.jpg', shell=True)
            await update.message.reply_photo(open("/media/pics/img.jpg", 'rb'), "зашакалено")
    elif ogg:
        print(datetime.now().strftime("%d.%m.%Y %X"), "шакалю голосовое")
        await update.message.reply_chat_action('record_voice')
        subprocess.run('ffmpeg -loglevel quiet -y -i /media/voice.ogg -vn -c:a libopus -ar 8000 -ab 500 /media/voioice.ogg', shell=True)
        await update.message.reply_voice(open("/media/voioice.ogg", 'rb'))

async def манул(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action("typing")
    print(datetime.now().strftime("%d.%m.%Y %X"), "считаю манулов")
    num = int(float(subprocess.getoutput('awk \'{print $1/60}\' /proc/uptime')))
    if (num%10==1):
        suffix =' манул'
    elif (num%10==2 or num%10==3 or num%10==4):
        suffix =' манула'
    else:
        suffix =' манулов'
    msgtxt = str(num) + suffix
    random.seed()
    num = random.randint(0,1)
    if (num==1):
        await update.message.reply_chat_action('record_voice')
        f = open('/media/manul.txt', 'w')
        f.write(msgtxt)
        f.close()
        subprocess.run('cat /media/manul.txt | RHVoice-test -p pavel -o /media/manul.ogg', shell=True)
        await update.message.reply_voice(open("/media/manul.ogg", 'rb'))
    else:
        await update.message.reply_text(msgtxt)

async def glitch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    надоли = False
    if update.message.reply_to_message is not None:
        mid = update.message.reply_to_message
        if mid.sticker:
            if not (mid.sticker.is_animated or mid.sticker.is_video):
                file = await mid.sticker.get_file()
                надоли = True
            else:
                await update.message.reply_chat_action('typing')
                print(datetime.now().strftime("%d.%m.%Y %X"), "отказываю глитчить анимированный стикер")
                await update.message.reply_text('я могу глитчить только статичные изображения')
                return
        elif mid.photo:
            file = await mid.photo[-1].get_file()
            надоли = True
    else:
        file = await update.message.photo[-1].get_file()
        надоли = True
    if надоли:
        await update.message.reply_chat_action('upload_photo')
        await file.download_to_drive("/media/pics/image.jpg")
        print(datetime.now().strftime("%d.%m.%Y %X"), "глитчу в жепег")
        gl = ImageGlitcher()
        glr=gl.glitch_image('/media/pics/image.jpg', 5.5, color_offset=True)
        glr.save('/media/pics/gl.jpg')
        await update.message.reply_photo(open("/media/pics/gl.jpg", 'rb'), "сглитчено")

async def glitch_gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    надоли = False
    if update.message.reply_to_message is not None:
        mid = update.message.reply_to_message
        if mid.sticker:
            if not (mid.sticker.is_animated or mid.sticker.is_video):
                file = await mid.sticker.get_file()
                надоли = True
            else:
                await update.message.reply_chat_action('typing')
                print(datetime.now().strftime("%d.%m.%Y %X"), "отказываю глитчить анимированный стикер")
                await update.message.reply_text('я могу глитчить только статичные изображения')
                return
        elif mid.photo:
            file = await mid.photo[-1].get_file()
            надоли = True
    else:
        file = await update.message.photo[-1].get_file()
        надоли = True
    if надоли:
        await update.message.reply_chat_action('upload_photo')
        await file.download_to_drive("/media/pics/image.jpg")
        print(datetime.now().strftime("%d.%m.%Y %X"), " глитчу в гифку")
        gl = ImageGlitcher()
        glr=gl.glitch_image('/media/pics/image.jpg', 5.5, color_offset=True, gif = True)
        glr[0].save('/media/pics/gl.gif', format = 'GIF', append_images = glr[1:], save_all = True, duration = 200, loop = 0)
        await update.message.reply_animation(open("/media/pics/gl.gif", 'rb'), "сглитчено в гифку")

async def videos_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    надоли = False
    if ((update.message is not None) and (hasattr(update.message, 'caption'))):
        msgtxt = update.message.caption
        if (msgtxt is not None):
            надоли = ("датамош" in msgtxt.lower() or "жмых" in msgtxt.lower())
            if надоли:
                if ("датамош" in msgtxt.lower()): await datamosh(update, context)
                elif (update.message.chat.id == 4dm1n): await видеожмых(update, context)

async def datamosh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "датамош видео просят")
    try:
        file = await update.message.video.get_file()
    except BadRequest as b:
        if "File is too big" in b.message:
            await update.message.reply_photo("AgACAgIAAxkBAAI6zWOUYYLKakHZMDc6XgqlEvUua-woAAKXwzEbDH6hSFw4yqcnveymAQADAgADeAADKwQ", "ботам не дают файлы больше 20 Мб")
            print(datetime.now().strftime("%d.%m.%Y %X"), "дали файл больше 20 Мб")
        else: print(datetime.now().strftime("%d.%m.%Y %X"), b.message)
    else:
        await file.download_to_drive("/media/vidos.mp4")
        induration = int(float(subprocess.getoutput('ffprobe -loglevel quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /media/vidos.mp4')))
        if induration > 90:
            await update.message.reply_chat_action('typing')
            print(datetime.now().strftime("%d.%m.%Y %X"), "отказал")
            await update.message.reply_text("слишком длинно (больше 90 секунд не буду датамошить)")
        else: 
            await update.message.reply_chat_action('typing')
            print(datetime.now().strftime("%d.%m.%Y %X"), "таки пытаюсь датамошить")
            await update.message.reply_text("ух бля. помолимся для стабильности интернет-канала и поставим свечку за здравие моих вычислительных мощностей %)")
            outduration = 3 + induration
            await update.message.reply_chat_action('upload_video')
            subprocess.run('ffmpeg -loglevel quiet -y -i /media/vidos.mp4 -crf 0 -pix_fmt yuv420p -r 25 /media/vidos.avi', shell=True)
            inp_file = open('/media/vidos.avi', 'rb')
            out_file = open('/media/vidosmoshed.avi', 'wb')
            inp_file_bytes = inp_file.read()
            await update.message.reply_chat_action('upload_video')
            frames = inp_file_bytes.split(bytes.fromhex('30306463'))
            iframe = bytes.fromhex('0001B0')
            i_frame_yet = False
            for index, frame in enumerate(frames):
                if i_frame_yet==False or index < 75 or index > 150:
                    out_file.write(frame + bytes.fromhex('30306463'))
                    if frame[5:8] == iframe: i_frame_yet = True
                else:
                    if frame[5:8] != iframe:
                        for i in range(15):
                            out_file.write(frame + bytes.fromhex('30306463'))
            inp_file.close()
            out_file.close()
            await update.message.reply_chat_action('upload_video')
            sc = ' -loglevel quiet -y -i /media/vidosmoshed.avi -crf 18 -pix_fmt yuv420p -vcodec libx264 -acodec aac -r 25 -to ' + str(outduration) + ' /media/vidosmoshed.mp4'
            subprocess.run(['ffmpeg' + sc], shell=True)
            await update.message.reply_chat_action('upload_video')
            await update.message.reply_video(open("/media/vidosmoshed.mp4", 'rb'))

async def jew(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    num = random.randrange(0,10001)
    if (num%99==0):
        await update.message.reply_chat_action('typing')
        print(datetime.now().strftime("%d.%m.%Y %X"), "таки почему")
        await update.message.reply_text("а таки почему ви спrашиваете?")

async def дела_сыча(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action("typing")
    hours = int(float(subprocess.getoutput('awk \'{print $1/3600}\' /proc/uptime')))
    days = str(hours//24)
    suthours = hours - int(days)*24
    num = random.randrange(0,3)
    if (hours%10==1): substr = " час"
    elif (hours%10==2 or hours%10==3 or hours%10==4): substr = " час+а"
    else: substr = " часов"
    if (suthours%10==1): substr2 = " час"
    elif (suthours%10==2 or suthours%10==3 or suthours%10==4): substr2 = " час+а"
    else: substr2 = " часов"
    t = subprocess.check_output("sensors", text=True)[53:58]
    msgtxt = "ну, бля, как-то так: я без остановки ебашу уже " + str(hours) + substr + ", это примерно " + days + " суток и " + str(hours%24) + substr2 + ". А ещё у меня температура " + t + ", а тут эти блядские манулы каждую минуту шароёбятся, а мне их считать ещё надо. Пиздец, короче!"
    if (num!=1):
        print(datetime.now().strftime("%d.%m.%Y %X"), "жалуюсь")
        await update.message.reply_text(msgtxt)
    else:
        print(datetime.now().strftime("%d.%m.%Y %X"), "жалуюсь вслух")
        await update.message.reply_chat_action('record_voice')
        f = open('/media/dela.txt', 'w')
        f.write(msgtxt)
        f.close()
        subprocess.run('cat /media/dela.txt | RHVoice-test -p pavel -o /media/dela.ogg', shell=True)
        await update.message.reply_voice(open("/media/dela.ogg", 'rb'))

async def видеожмых(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "видеожмых")
    file = await update.message.video.get_file()
    await file.download_to_drive("/media/videozh/vidoszh.mp4")
    await update.message.reply_text("я, конечно, попробую, но если файл больше 20 Мб, то ничего не выйдет точно. таковы ограничения для ботов.")
    duration = int(float(subprocess.getoutput('ffprobe -loglevel quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /media/videozh/vidoszh.mp4')))
    if (duration > 90):
        await update.message.reply_text("не буду жмыхать")
    else:
        subprocess.run('ffmpeg -loglevel quiet -y -i /media/videozh/vidoszh.mp4 /media/videozh/frames/%05d.jpg', shell=True)
        subprocess.run('ffmpeg -loglevel quiet -y -i /media/videozh/vidoszh.mp4 -vn -c:a copy /media/videozh/vidoszh.aac', shell=True)
        subprocess.run('ffmpeg -loglevel quiet -y -i /media/videozh/vidoszh.aac -vn -c:a aac -af vibrato=f=10:d=1 /media/videozh/viidoszh.aac', shell=True)
        num = len(glob.glob('/media/videozh/frames/*'))
        i=1
        while i < num+1:
            tempstr = ' -limit memory 1536MiB /media/videozh/frames/' + str(i).zfill(5) + '.jpg -liquid-rescale 75% /media/videozh/frames/img' + str(i).zfill(5) + '.jpg'
            subprocess.run(['convert' + tempstr], shell=True)
            i+=1
        await update.message.reply_chat_action('upload_video')
        subprocess.run('ffmpeg -loglevel error -y -r 25 -i /media/videozh/frames/img%05d.jpg -i /media/videozh/viidoszh.aac -r 25 /media/videozh/zh.mp4', shell=True)
        subprocess.run('rm -rf /media/videozh/frames/*', shell=True)
        await update.message.reply_video(open("/media/videozh/zh.mp4", 'rb'))

async def в_базу(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msgtxt = update.message.text
    userid = update.message.from_user.id
    con = sqlite3.connect("/media/db/messages.db")
    cur = con.cursor()
    cur.execute("INSERT INTO messages VALUES(?, ?)", (userid, msgtxt))
    con.commit()
    con.close()

async def из_базы(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action("typing")
    userid = update.message.from_user.id
    con = sqlite3.connect("/media/db/messages.db")
    cur = con.cursor()
    res = cur.execute("SELECT text FROM messages WHERE userid=?", (userid,))
    vybor = res.fetchall()
    con.close()
    if len(vybor)>19:
        num = random.randint(0, len(vybor)-1)
        await update.message.reply_text(str(vybor[num][0]))
    elif random.randint(0,1)==1: await update.message.reply_text("я тебя ещё плохо знаю, чтобы придумать ответ.")
    else: await update.message.reply_sticker("CAACAgIAAxkBAAJcBGPmxtaU1DqaSgaDyK1uG8bJDtIuAAJTLAACC0AxS9-hjzZ0eEdZLgQ")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    logger.error(f"Обосрамс: {error}, тип: {type(error).__name__}")
    #logger.error("fffuuu:", exc_info=context.error)

async def qq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    await file.download_to_drive("/media/qq/imageqq.jpg")
    print(datetime.now().strftime("%d.%m.%Y %X"), "qq")
    with open("/media/qq/imageqq.jpg", "rb") as imgtoqq:
        toqq = base64.b64encode(imgtoqq.read())
    tojsonstr = toqq.decode()
    json_data = {
    "busiId": "different_dimension_me_img_entry",
    "images": [tojsonstr],
    "extra": "{\"face_rects\":[],\"version\":2,\"platform\":\"web\",\"data_report\":{\"parent_trace_id\":\"25927d33-98e1-0e0d-f0e2-42fd48389ef9\",\"root_channel\":\"\",\"level\":1}}",
    }
    value = f"https://h5.tu.qq.com{len(json_data)}HQ31X02e"
    value = hashlib.md5(value.encode()).hexdigest()
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'x-sign-value': str(value),
    'x-sign-version': 'v1',
    'Origin': 'https://h5.tu.qq.com',
    'Referer': 'https://h5.tu.qq.com/',
    }
    r = requests.post('https://ai.tu.qq.com/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process', headers=headers, json=json_data,)
    fromqq = r.content.decode('utf8').replace("'", '"')
    jfromqq = json.loads(fromqq)
    print(jfromqq)
    neededpart = jfromqq['extra']
    reallyneededpart  = json.loads(neededpart)
    urls = reallyneededpart['img_urls']
    url1 = urls[0]
    url2 = urls[1]
    url3 = urls[2]
    url4 = urls[3]
    resp1 = requests.get(url1)
    open("/media/qq/qq1.jpg", "wb").write(resp1.content)
    resp2 = requests.get(url2)
    open("/media/qq/qq2.jpg", "wb").write(resp2.content)
    resp3 = requests.get(url3)
    open("/media/qq/qq3.jpg", "wb").write(resp3.content)
    resp4 = requests.get(url4)
    open("/media/qq/qq4.jpg", "wb").write(resp4.content)
    await update.message.reply_photo(open("/media/qq/qq1.jpg", "rb"), "раз")
    await update.message.reply_photo(open("/media/qq/qq2.jpg", "rb"), "джва")
    await update.message.reply_photo(open("/media/qq/qq3.jpg", "rb"), "три")
    await update.message.reply_photo(open("/media/qq/qq4.jpg", "rb"), "четыре")

async def нахуй(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action("typing")
    print(datetime.now().strftime("%d.%m.%Y %X"), "посылаю нахуй")
    await update.message.reply_text("кусай за хуй")

async def хуй_на(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action("typing")
    print(datetime.now().strftime("%d.%m.%Y %X"), "предлагаю хуй")
    await update.message.reply_text("хуй на")

async def жуй_два(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action("typing")
    print(datetime.now().strftime("%d.%m.%Y %X"), "предлагаю два хуя")
    await update.message.reply_text("жуй два")

async def жуй_четыре(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action("typing")
    print(datetime.now().strftime("%d.%m.%Y %X"), "предлагаю четыре хуя")
    await update.message.reply_text("жуй четыре — у тебя ебало шире")

async def dice_answerer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ((update.message.dice.emoji == "🎯" and update.message.dice.value == 1) or (update.message.dice.emoji == "🏀" and update.message.dice.value < 4) or (update.message.dice.emoji == "⚽" and update.message.dice.value < 3) or (update.message.dice.emoji == "🎳" and update.message.dice.value == 1)):
        await update.message.reply_chat_action("typing")
        print(datetime.now().strftime("%d.%m.%Y %X"), "хуесошу за промахи")
        await update.message.reply_text("мазила")
    elif (update.message.dice.emoji == "🎯" and update.message.dice.value == 6):
        await update.message.reply_chat_action("typing")
        print(datetime.now().strftime("%d.%m.%Y %X"), "хвалю дротиста")
        await update.message.reply_text("в яблочко!")
    elif (update.message.dice.emoji == "🎳" and update.message.dice.value == 6):
        await update.message.reply_chat_action("typing")
        print(datetime.now().strftime("%d.%m.%Y %X"), "хвалю боулингиста")
        await update.message.reply_text("страйк!")
    elif (update.message.dice.emoji == "🏀" and update.message.dice.value > 3):
        await update.message.reply_chat_action("choose_sticker")
        print(datetime.now().strftime("%d.%m.%Y %X"), "хвалю баскетболиста")
        await update.message.reply_sticker("CAACAgIAAxkBAAI702OXQmMY52EsMiA8Jm8gpNirCU2PAAIKEgACzQLoS-Ogs8jlrGv0KwQ")
    elif (update.message.dice.emoji == "⚽" and update.message.dice.value > 2):
        await update.message.reply_chat_action("typing")
        print(datetime.now().strftime("%d.%m.%Y %X"), "хвалю футболиста")
        await update.message.reply_text("гооол!")
    elif (update.message.dice.emoji == "🎰" and (update.message.dice.value == 22 or update.message.dice.value == 43)):
        await update.message.reply_chat_action("typing")
        print(datetime.now().strftime("%d.%m.%Y %X"), "хвалю лудомана")
        await update.message.reply_text("👏")
    elif (update.message.dice.emoji == "🎰" and update.message.dice.value == 1):
        await update.message.reply_chat_action("upload_document")
        print(datetime.now().strftime("%d.%m.%Y %X"), "поцелуй мою залупу")
        await update.message.reply_animation("CgACAgIAAxkBAAI8E2OXRubJFHJtLWBlqVB6X_XtzMDqAAIwHAACGGG5S0wHqqoAAW9qSysE")
    elif (update.message.dice.emoji == "🎰" and update.message.dice.value == 64):
        await update.message.reply_chat_action("typing")
        print(datetime.now().strftime("%d.%m.%Y %X"), "джекпот")
        await update.message.reply_markdown_v2("ебать\! джекпот\! джекпот\! ||хуй те в рот||")

async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action('upload_photo')
    print(datetime.now().strftime("%d.%m.%Y %X"), "кица")
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    j = r.json()
    ссылка = j[0]["url"]
    #print(ссылка)
    if ссылка.endswith("gif"): await update.message.reply_animation(ссылка)
    elif ссылка.endswith(("jpg", "png", "jpeg")): await update.message.reply_photo(ссылка)
    else: await update.message.reply_text(j[0]["url"])

async def dog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action('upload_photo')
    print(datetime.now().strftime("%d.%m.%Y %X"), "песц")
    r = requests.get("https://api.thedogapi.com/v1/images/search")
    j = r.json()
    ссылка = j[0]["url"]
    #print(ссылка)
    if ссылка.endswith("gif"): await update.message.reply_animation(ссылка)
    elif ссылка.endswith(("jpg", "png", "jpeg")): await update.message.reply_photo(ссылка)
    else: await update.message.reply_text(j[0]["url"])

async def neko(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action('upload_photo')
    print(datetime.now().strftime("%d.%m.%Y %X"), "кошкодевка")
    r = requests.get("https://nekos.best/api/v2/neko")
    j = r.json()
    ссылка = j["results"][0]["url"]
    #print(ссылка)
    if ссылка.endswith("gif"): await update.message.reply_animation(ссылка)
    elif ссылка.endswith(("jpg", "png", "jpeg")): await update.message.reply_photo(ссылка)
    else: await update.message.reply_text(j["results"][0]["url"])

async def duck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action('upload_photo')
    print(datetime.now().strftime("%d.%m.%Y %X"), "утка")
    r = requests.get("https://random-d.uk/api/v2/random")
    j = r.json()
    ссылка = j["url"]
    #print(ссылка)
    if ссылка.endswith("gif"): await update.message.reply_animation(ссылка)
    elif ссылка.endswith(("jpg", "png", "jpeg")): await update.message.reply_photo(ссылка)
    else: await update.message.reply_text(j["url"])

async def мандаринка(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action('record_video_note')
    print(datetime.now().strftime("%d.%m.%Y %X"), "мандаринка")
    await update.message.reply_text("""🌕🌕🌕🌕🌕🌕🌕🌕
🌕🌕🌕🌕🌕🎩🌕🌕
🌕🌕🌕🌕🌘🌑🌒🌕
🌕🌕🌕🌘🌑🌑🌑🌓
🌕🌕🌖🌑👁👃🏻👁🌓     
🌕🌕🌗🌑🌑👄🌑🌔
🌕🌕🌘🌑🌑🌑🌒🌕 💬БУДЕШЬ
🌕🌕🌘👉🏻🍊👈🏻🌓🌕       МАНДАРИНКУ?
🌕🌕🌘🌑🌑🌑🌔🌕
🌕🌕🌘🌔🌘🌑🌕🌕
🌕🌕🌗🌔🌗🌒🌕🌕
🌕🌕🌗🌔🌗🌓🌕🌕
🌕🌕🌘🌔🌗🌓🌕🌕
🌕🌕👠🌕🌕👠🌕🌕""")

''' async def балабоба(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action('typing')
    print(datetime.now().strftime("%d.%m.%Y %X"), "балабоблю")
    if ((update.message is not None) and (hasattr(update.message, 'text'))):
        ии = True
        if (update.message.reply_to_message is not None):
            mid = update.message.reply_to_message
            if mid.text is not None: msgtxt = mid.text
            elif mid.caption is not None: msgtxt = mid.caption
            else: 
                ии = False
                await update.message.reply_text("балабобить можно только текст. здесь текста нет. как я туда передам пустоту?")
        else:
            msgtxt = update.message.text
    if ии:
        if "/b@kookoomyawka_bot" in msgtxt: msgtxt=msgtxt.removeprefix("/b@kookoomyawka_bot")
        else: msgtxt=msgtxt.removeprefix("/b")
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://yandex.com',
        'Content-Type': 'application/json',
        'Origin': 'https://yandex.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        }
        json_data = {'query':f'{msgtxt}', 'intro': 0, 'filter': 0}
        if len(msgtxt)>0:
            r = requests.post('https://zeapi.yandex.net/lab/api/yalm/text3', headers=headers, json=json_data, verify=False,)
            j = r.json()
            if j['bad_query']==1: await update.message.reply_text('Балабоба не принимает запросы на острые темы, например, про политику или религию. Люди могут слишком серьёзно отнестись к сгенерированным текстам. Вероятность того, что запрос задаёт одну из острых тем, определяет нейросеть, обученная на оценках случайных людей. Но она может перестараться или, наоборот, что-то пропустить.')
            else: await update.message.reply_text(j['text'])
        else: await update.message.reply_text('после /b надо бы написать какой-то текст.') '''

async def remember_kb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "напоминаю")
    keyboard = [
        [
            InlineKeyboardButton("Выкл. PC", callback_data="shutdown"),
            InlineKeyboardButton("Вкл. PC", callback_data="wake_pc"),
            InlineKeyboardButton("Кто в сети?", callback_data="кто_в_сети"),
        ],
        [
            InlineKeyboardButton("Свет", callback_data="вкл_экран"),
            InlineKeyboardButton("Скрин", callback_data="screen"),
            InlineKeyboardButton("Фото", callback_data="photo"),
        ],
        [
            InlineKeyboardButton("IP-адрес", callback_data="ip"),
            InlineKeyboardButton("Аптайм", callback_data="uptime"),
            InlineKeyboardButton("Температура", callback_data="temp"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("/shutdownrainbow   /wakepc   /light   /screen   /photo   /ip   /uptime   /temp   /whosthere", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data=='shutdown': await shutdown(update, context)
    elif query.data=='wake_rainbow': await wake_pc(update, context)
    elif query.data=='кто_в_сети': await кто_в_сети(update, context)
    elif query.data=='вкл_экран': await вкл_экран(update, context)
    elif query.data=='screen': await screen(update, context)
    elif query.data=='photo': await photo(update, context)
    elif query.data=='ip': await pc_ip(update, context)
    elif query.data=='uptime': await pc_uptime(update, context)
    elif query.data=='temp': await pc_temp(update, context)

async def бахнем(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "бахнем")
    await update.message.reply_chat_action("typing")
    await update.message.reply_text("обязательно бахнем! и не раз! весь мир в труху!.. но потом.")

async def button_for_roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ammo = int(query.data)
    armed = set()
    num = random.randint(1, 6)
    if query.data=="0": 
        print(datetime.now().strftime("%d.%m.%Y %X"), "зарядить забыл")
        await query.edit_message_caption(caption="Ты решил поиграть в рулетку с нулём патронов в барабане. Ты их, что, забыл?")
    elif query.data=="6":
        print(datetime.now().strftime("%d.%m.%Y %X"), "6 из 6")
        await query.edit_message_caption(caption="шесть из шести? больше похоже на попытку самовыпила, чем на игры. очевидно, что скурткобейнился.")
    else:
        print(datetime.now().strftime("%d.%m.%Y %X"), "заряжено", query.data, "патронов")
        while (len(armed)<ammo):
            armed.add(random.randint(1,6))
        print(datetime.now().strftime("%d.%m.%Y %X"), "патроны в каморах ", armed)
        if (num in armed):
            print(datetime.now().strftime("%d.%m.%Y %X"), "rip")
            capstr = "патроны в каморах № " + str(armed) + ". \nбоёк ударил по каморе №" + str(num) + ", но она была не пуста. ты скурткобейнился."
            await query.edit_message_caption(caption=capstr)
        else:
            print(datetime.now().strftime("%d.%m.%Y %X"), "жив")
            capstr = "патроны в каморах: " + str(armed) + ". \nбоёк ударил по каморе №" + str(num) + ", а она была пуста. выстрела не произошло."
            await query.edit_message_caption(caption=capstr)

async def roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "вращайте барабан!")
    await update.message.reply_chat_action("typing")
    keyboard = [
        [
            InlineKeyboardButton("0", callback_data=0),
            InlineKeyboardButton("1", callback_data=1),
            InlineKeyboardButton("2", callback_data=2),
            InlineKeyboardButton("3", callback_data=3),
            InlineKeyboardButton("4", callback_data=4),
            InlineKeyboardButton("5", callback_data=5),
            InlineKeyboardButton("6", callback_data=6),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_animation("CgACAgIAAxkBAAIKZmK_MikcDAAB3BCAfodCbbDC_Yo-YgACohwAAqmu-EnUGhAtgOu5uCkE", caption="вращайте барабан!", reply_markup=reply_markup)

async def шар_восьмёрка(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "🎱")
    await update.message.reply_chat_action("record_video_note")
    ответ = random.choice(['бесспорно', 'предрешено', 'никаких сомнений', 'определённо — да', 'инфа сотка', 'ящитаю, што да', 'вероятнее всего', 'это возможно', 'знаки говорят — да', 'агась', 'пока не ясно, попробуй снова', 'спроси позже', 'не сейчас', 'сейчас нельзя предсказать', 'сконцентрируйся и спроси опять', 'даже не думай', 'весьма сомнительно', 'перспективы не очень хорошие', 'не надейся на это', 'забудь об этом'])
    await update.message.reply_text('ответ на твой вопрос: ' + ответ)

async def stickers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ((update.message.reply_to_message is not None) and (hasattr(update.message, 'from_user'))):
            forme = update.message.reply_to_message.from_user.id == 5441337742
            if forme:
                if update.message.sticker.file_unique_id=="AgADZQEAAnY3dj8" or update.message.sticker.file_unique_id=="AgAD2CsAAjTrKUs":
                    await update.message.reply_chat_action("choose_sticker")
                    print(datetime.now().strftime("%d.%m.%Y %X"), "😎")
                    await update.message.reply_sticker("CAACAgIAAxkBAAJcA2PmxjoWJjLvWPUH0Z-hBlPWhQmaAALYKwACNOspS9LSWkSb6FCyLgQ")
                else:
                    await update.message.reply_chat_action("choose_sticker")
                    num = random.randint(0,1)
                    if (num==1):
                        print(datetime.now().strftime("%d.%m.%Y %X"), "отвечаю стикером на стикер")
                        стикер = random.choice(["CAACAgIAAxkBAAJGvWOrJgJU-BkdAbzGd06nJvEr1jCEAAIRJQAC6fRgSYPaxu4saJY8LAQ", "CAACAgIAAxkBAAJGvmOrJgauAeGFP9XvcaP_E25_LkdWAAISJQAC6fRgSe5o5ZlxmkZ5LAQ", "CAACAgIAAxkBAAJGv2OrJgs-FWbVXgURhsFUpq_aAbCDAAITJQAC6fRgSRfaOkfe0T0jLAQ"])
                        await update.message.reply_sticker(стикер)
                    else:
                        print(datetime.now().strftime("%d.%m.%Y %X"), "реплай из базы на стикер")
                        await из_базы(update, context)

async def праздники(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action('typing')
    print(datetime.now().strftime("%d.%m.%Y %X"), "праздники")
    r = requests.get("https://www.calend.ru/img/export/informer_new_3.js")
    resp = r.text
    resp = resp[resp.find("><a")+1:resp.rfind("><")+1]
    resp = resp.replace("target=_blank ", "")
    resp = resp.replace(" class=\"+calendru_mc+\"", "")
    resp = resp.replace(" class=\"+calendru_c+\"", "")
    resp = resp.replace("document.write(\"<div", "")
    resp = resp.replace("class=\"+calendru_c_all+\">\");", "")
    resp = resp.replace("</div>\");", "")
    resp = resp.replace("if(calendru_i_f) >", "")
    while "<span" in resp:
        resp = resp[:resp.find("<span")] + resp[resp.find("/span>")+5:]
    resp = resp.replace("><br>", "")
    resp = resp.replace("if(calendru_show_names) >> ", "Именины:  ")
    resp = resp.replace(" class=\"+calendru_c_names+\" ", "")
    resp = resp.replace("><a", "<a")
    resp = resp.replace("a>>", "a>")
    resp = resp.replace("  >", ">")
    resp = resp.replace(" >", ">")
    resp = resp.replace("/>", "/\">")
    resp = resp.replace("href=", "href=\"")
    resp = resp.replace("\n\n", "\n")
    msgtxt = "Праздники сегодня, "
    await update.message.reply_html(msgtxt+resp)

'''async def chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "chatgpt")
    await update.message.reply_chat_action('typing')
    ии = True
    openai.api_key = "op-AIapiK3y"
    if (update.message.reply_to_message is not None):
        mid = update.message.reply_to_message
        if mid.text is not None: msgtxt = mid.text
        elif mid.caption is not None: msgtxt = mid.caption
        else: 
            ии = False
            await update.message.reply_text("в ChatGPT можно передать только текст. здесь текста нет. как я туда передам пустоту?")
    else:
        msgtxt = update.message.text
    if ии:
        await update.message.reply_chat_action('typing')
        userid = "user" + str(update.message.from_user.id)
        if "/c@kookoomyawka_bot" in msgtxt: msgtxt=msgtxt.removeprefix("/c@kookoomyawka_bot")
        else: msgtxt=msgtxt.removeprefix("/c")
        if len(msgtxt)>0:
            await update.message.reply_chat_action('typing')
            completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content":f'{userid} said: {msgtxt}'}])
            await update.message.reply_text(completion.choices[0].message.content)
        else: await update.message.reply_text('после /c надо бы написать какой-то текст.')
    print(datetime.now().strftime("%d.%m.%Y %X") + " " + str(update.message.chat.id) +": " + msgtxt, file=open('/media/db/gpt.txt', 'a'))  '''

async def getf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    надоли = False
    print(datetime.now().strftime("%d.%m.%Y %X"), "даю file_id")
    await update.message.reply_chat_action('find_location')
    if update.message.reply_to_message is not None:
        mid = update.message.reply_to_message
        if mid.sticker:
            msgtxt = mid.sticker.file_id
            надоли = True
        elif mid.animation:
            msgtxt = mid.animation.file_id
            надоли = True
        elif mid.document:
            msgtxt = mid.document.file_id
            надоли = True
        elif mid.video:
            msgtxt = mid.video.file_id
            надоли = True
        elif mid.video_note:
            msgtxt = mid.video_note.file_id
            надоли = True
        elif mid.voice:
            msgtxt = mid.voice.file_id
            надоли = True
        elif mid.audio:
            msgtxt = mid.audio.file_id
            надоли = True
        else: надоли = False
    if надоли: await update.message.reply_html(f'<code>{msgtxt}</code>')
    else: await update.message.reply_html('ты делаешь это неправильно')

'''async def catboys(update: Update, context: ContextTypes.DEFAULT_TYPE): #не используется, ибо домен стух
    await update.message.reply_chat_action('upload_photo')
    print(datetime.now().strftime("%d.%m.%Y %X"), "catboy")
    r = requests.get("https://api.catboys.com/img")
    j = r.json()
    ссылка = j["url"]
    #print(ссылка)
    if ссылка.endswith("gif"): await update.message.reply_animation(ссылка)
    elif ссылка.endswith(("jpg", "png", "jpeg")): await update.message.reply_photo(ссылка)
    else: await update.message.reply_text(j["url"])  '''

async def елда(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "елда")
    await update.message.reply_chat_action('typing')
    await update.message.reply_html('да уж получше твоей, бесхуее создание')

async def d20(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "d20")
    await update.message.reply_text('d20: ' + str(random.randint(1, 20)))

async def d4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "d4")
    await update.message.reply_text('d4: ' + str(random.randint(1, 4)))

async def d6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "d6")
    await update.message.reply_text('d6: ' + str(random.randint(1, 6)))

async def d8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "d8")
    await update.message.reply_text('d8: ' + str(random.randint(1, 8)))

async def d10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "d10")
    await update.message.reply_text('d10: ' + str(random.randint(1, 10)))

async def d12(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "d12")
    await update.message.reply_text('d12: ' + str(random.randint(1, 12)))

async def d100(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "d100")
    await update.message.reply_text('d100: ' + str(random.randint(1, 100)))

async def d10x2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "d10x2")
    await update.message.reply_html('d10x2: ' + str(random.randint(0, 9)*10 + random.randint(0, 9)) + '\n <i>* 00 =  100 </i>')

async def boobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "booba")
    r = requests.get('http://api.oboobs.ru/boobs')
    j = r.json()
    id = j[0]["id"]
    number = str(random.randint(1, id)).zfill(5)
    link = 'http://media.oboobs.ru/boobs/' + number + '.jpg'
    await update.message.reply_photo(link)

async def torrent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    надоли = False
    print(datetime.now().strftime("%d.%m.%Y %X"), "получаю торрент-файл")
    await update.message.reply_chat_action('find_location')
    if update.message.reply_to_message is not None:
        mid = update.message.reply_to_message
        if mid.document:
            filename = mid.document.file_name
            надоли = True
            tfilepath = '/!tfiles/' + filename
            tfile = await mid.document.get_file()
            await tfile.download_to_drive(tfilepath)
    if надоли: await update.message.reply_html('торрент-то я закинул, а остальное зависит не от меня')
    else: await update.message.reply_html('ты делаешь это неправильно')

async def good_morning_old():
    random.seed()
    rbo = requests.get('http://api.oboobs.ru/boobs')
    jbo = rbo.json()
    idbo = jbo[0]["id"]
    number = str(random.randint(1, idbo)).zfill(5)
    linkbo = 'http://media.oboobs.ru/boobs/' + number + '.jpg'
    testbo = requests.get(linkbo)
    while testbo.status_code != 200:
        random.seed()
        number = str(random.randint(1, idbo)).zfill(5)
        linkbo = 'http://media.oboobs.ru/boobs/' + number + '.jpg'
        testbo = requests.get(linkbo)
    random.seed()
    rbu = requests.get('http://api.obutts.ru/butts')
    jbu = rbu.json()
    idbu = jbu[0]["id"]
    number = str(random.randint(1, idbu)).zfill(5)
    linkbu = 'http://media.obutts.ru/butts/' + number + '.jpg'
    testbu = requests.get(linkbu)
    while testbu.status_code != 200:
        random.seed()
        number = str(random.randint(1, idbu)).zfill(5)
        linkbu = 'http://media.obutts.ru/butts/' + number + '.jpg'
        testbu = requests.get(linkbu)
    await Bot('L0NG:B07-70KEN').send_media_group(chat_id=-needed_chat_id, caption='Доброе утро, милостивые господа!', media=[InputMediaPhoto(media=linkbo), InputMediaPhoto(media=linkbu)])

async def butt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed()
    print(datetime.now().strftime("%d.%m.%Y %X"), "butt")
    r = requests.get('http://api.obutts.ru/butts')
    j = r.json()
    id = j[0]["id"]
    number = str(random.randint(1, id)).zfill(5)
    link = 'http://media.obutts.ru/butts/' + number + '.jpg'
    await update.message.reply_photo(link)

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "запросили инфу по донатам")
    await update.message.reply_html("Донаты через\nTON: <code>UQCI23tiAAPjI7m8BpiVBnpaelPrtsdPMk4xwqhhOzX6nN_7</code>\nUSDT: <code>TJEDJvGff7JY4HV6mr8qb8fH8zAF1xaXfC</code>\nBTC: <code>1LkBaQUg3ZDfGknvkQzH6CHmV5VHEe7prd</code>")

async def триста(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "предлагаю пососать за 300")
    await update.message.reply_chat_action('typing')
    ответ = "отсоси у "
    выбор = random.choice(['тракториста', 'моториста', 'трубочиста', 'программиста', 'говночиста', 'баяниста', 'питониста', 'альпиниста', 'гитариста', 'хоккеиста', 'массажиста', 'террориста', 'фетишиста', 'лицеиста', 'гуманиста', 'онаниста', 'митолизда', 'коммуниста', 'гедониста', 'моралиста', 'теннисиста', 'эгоиста', 'вокалиста', 'оптимиста', 'каратиста', 'сценариста', 'шахматиста', 'гармониста', 'бейсболиста', 'пейзажиста', 'анархиста', 'всех в этом чате, пожалуйста'])
    await update.message.reply_text(ответ+выбор)

async def novichok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.id == -needed_chat_id:
        random.seed()
        what = random.randint(0,1)
        if what:
            anim = random.choice(['CgACAgQAAxkBAAEB5VNlmH44Gmq1bYyzi8wQmpaDy0WKYgACCRAAAofUCFOudyt-U-MmlDQE','CgACAgIAAxkBAAEB5VllmH7gOW0SzMDOlbnApgRqK3sIuAACzjoAAnDNuEjx2LWKxjNa8DQE','CgACAgQAAxkBAAEB5VxlmH-HSW1gWgTxhxSdcG1xmJ4xQgACCxAAAofUCFPvB_tHEfJzSDQE','CgACAgQAAxkBAAEB5V5lmH-H9BB2IpRoqxiPuTs6j9FshAACBhAAAofUCFO9pJTDXgkBHzQE','CgACAgIAAxkBAAEB5V1lmH-HebARo3pzf0KkYKK6s5izfgACPz4AAnemQUiHYhkQhujEOjQE'])
            await update.message.reply_animation(anim)
            print(datetime.now().strftime("%d.%m.%Y %X"), "приветствую новичка у xxxx гифкой")
        else:
            await update.message.reply_photo("AgACAgIAAxkBAAEB5YplmImTbzOIo0oF4wfyIbnq5sAySgACy9ExG5ipsUiP9XZGBeOYcAEAAwIAA3MAAzQE")
            print(datetime.now().strftime("%d.%m.%Y %X"), "приветствую новичка у xxxx пикчей")
    elif update.message.chat.id == -1001640866252:
        unwanted = update.message.from_user.id
        доколе = int(t.time()) + 60
        await Bot('L0NG:B07-70KEN').ban_chat_member(-1001640866252, unwanted, доколе)

async def удоли(каво, где):
    await Bot('L0NG:B07-70KEN').delete_message(где, каво)
    print(datetime.now().strftime("%d.%m.%Y %X"), "чистию за собой")

async def ban_roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    каво = update.message.from_user.id
    доколе = int(t.time()) + 60
    где = update.message.chat.id
    print(datetime.now().strftime("%d.%m.%Y %X"), "самобан-рулетка")
    random.seed()
    armed = random.randint(1,6)
    random.seed()
    num = random.randint(1,6)
    if (num == armed):
        try: await Bot('L0NG:B07-70KEN').ban_chat_member(где, каво, доколе)
        except BadRequest as b:
            #print(b)
            if "Chat_admin_required" or "Not enough" in b.message: 
                await update.message.reply_text("я бы тебя забанил, будь у меня такие права.")
                print(datetime.now().strftime("%d.%m.%Y %X"), "не могу забанить")
        else:
            print(datetime.now().strftime("%d.%m.%Y %X"), "самобан")
            await update.message.reply_text("UWBFTP")
    else:
        print(datetime.now().strftime("%d.%m.%Y %X"), "жив")
        await update.message.reply_text("повезло-повезло")

async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "описываю действие")
    msgtxt = update.message.text
    who = update.effective_user
    if msgtxt == "/me" or msgtxt == "/me@kookoomyawka_bot": 
        try: await Bot('L0NG:B07-70KEN').delete_message(update.effective_chat.id, update.effective_message.message_id)
        except BadRequest as b:
            if "can't" in b.message:
                await update.message.reply_html(rf"{who.mention_html()} не понимает, как пользоваться /me")
        else: await Bot('L0NG:B07-70KEN').send_message(update.effective_chat.id, parse_mode="HTML", text=rf"*{who.mention_html()} не понимает, как пользоваться /me")
    elif ("/me@kookoomyawka_bot" in msgtxt): msgtxt=msgtxt.removeprefix("/me@kookoomyawka_bot ")
    else: msgtxt=msgtxt.removeprefix("/me ")
    try: await Bot('L0NG:B07-70KEN').delete_message(update.effective_chat.id, update.effective_message.message_id)
    except BadRequest as b:
        #print (b)
        if "can't" in b.message:
            await update.message.reply_html(rf"Это, конечно, и так видно, но {who.mention_html()} {msgtxt}")
    else: await Bot('L0NG:B07-70KEN').send_message(update.effective_chat.id, parse_mode="HTML", text=rf"*{who.mention_html()} {msgtxt}")
    

async def getID(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(datetime.now().strftime("%d.%m.%Y %X"), "даю id отправителя")
    if update.message.reply_to_message is not None:
        mid = update.message.reply_to_message
        if mid.sender_chat:
            msgtxt = mid.sender_chat.id
        await update.message.reply_html(f'<code>{msgtxt}</code>')
    else: await update.reply_text("you're doing it wrong")


def main():
    application = ApplicationBuilder().token('L0NG:B07-70KEN').build()
    
    планировщик.start()
    #планировщик.add_job(neural_horo, 'cron', hour=11, minute=11, timezone='TIMEZONE')
    планировщик.add_job(good_morning, 'cron', hour=8, minute=21, timezone='TIMEZONE')
    #планировщик.add_job(good_morning, 'cron', hour=6, minute=44, timezone='TIMEZONE')
    #application.add_handler(CommandHandler('gm', good_morning))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("temp", pc_temp, filters.Chat([4dm1n])))
    application.add_handler(CommandHandler("ip", pc_ip, filters.Chat([4dm1n])))
    application.add_handler(CommandHandler("uptime", pc_uptime, filters.Chat([4dm1n])))
    application.add_handler(CommandHandler("shutdown", shutdown, filters.Chat([4dm1n])))
    application.add_handler(CommandHandler("wake", wake_rainbow, filters.Chat([4dm1n])))
    application.add_handler(CommandHandler("photo", photo, filters.Chat([4dm1n])))
    application.add_handler(CommandHandler("screen", screen, filters.Chat([4dm1n])))
    application.add_handler(CommandHandler("light", вкл_экран, filters.Chat([4dm1n])))
    application.add_handler(CommandHandler("whosthere", кто_в_сети, filters.Chat([4dm1n])))
    application.add_handler(CommandHandler("fadvice", advice))
    application.add_handler(CommandHandler("vadvice", voice_advice))
    application.add_handler(CommandHandler("coin", coin))
    application.add_handler(CommandHandler("roulette", roulette))
    application.add_handler(CommandHandler("answer", answer))
    application.add_handler(CommandHandler("anek", anek))
    application.add_handler(CommandHandler("voiceanek", voice_anek))
    application.add_handler(CommandHandler("cat", cat))
    application.add_handler(CommandHandler("dog", dog))
    application.add_handler(CommandHandler("duck", duck))
    application.add_handler(CommandHandler("neko", neko))
    #application.add_handler(CommandHandler("b", балабоба))
    application.add_handler(CommandHandler("8", шар_восьмёрка))
    application.add_handler(CommandHandler("p", праздники))
    application.add_handler(CommandHandler("add", добавить_пароль, filters.Chat([4dm1n])))
    application.add_handler(CommandHandler("search", показать_бд, filters.Chat([4dm1n])))
    #application.add_handler(CommandHandler("c", chatgpt))
    application.add_handler(CommandHandler("getf", getf))
    #application.add_handler(CommandHandler("catboy", catboys))
    application.add_handler(CommandHandler("d20", d20))
    application.add_handler(CommandHandler("d4", d4))
    application.add_handler(CommandHandler("d6", d6))
    application.add_handler(CommandHandler("d8", d8))
    application.add_handler(CommandHandler("d10", d10))
    application.add_handler(CommandHandler("d12", d12))
    application.add_handler(CommandHandler("d100", d100))
    application.add_handler(CommandHandler("d10x2", d10x2))
    application.add_handler(CommandHandler("boobs", boobs))
    application.add_handler(CommandHandler("butt", butt))
    application.add_handler(CommandHandler("otherPC", otherPC, filters.Chat([4dm1n, otheradmin])))
    application.add_handler(CommandHandler("torrent", torrent, filters.Chat([4dm1n])))
    application.add_handler(CommandHandler("donate", donate))
    application.add_handler(CommandHandler("babe", babe))
    application.add_handler(CommandHandler("ban_roulette", ban_roulette))
    application.add_handler(CommandHandler("me", me))
    application.add_handler(CommandHandler("getid", getID))
    application.add_handler(MessageHandler((filters.PHOTO), pics_handler, True))
    application.add_handler(MessageHandler((filters.VIDEO), videos_handler, True))
    application.add_handler(MessageHandler((filters.TEXT & (~filters.COMMAND)), text_recognizer, True))
    application.add_handler(MessageHandler(filters.Dice.ALL, dice_answerer))
    application.add_handler(MessageHandler(filters.Sticker.ALL, stickers_handler))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, novichok))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_error_handler(error_handler)
    #application.add_error_handler(wtf)
    application.add_handler(CallbackQueryHandler(button, pattern="\D"))
    application.add_handler(CallbackQueryHandler(button_for_roulette, pattern="\d"))
    application.run_polling()

if __name__ == '__main__':
    main()
