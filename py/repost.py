# скрипт для репоста записей из ВК в ТГ силами своего тг-бота*, запускается ручками после постинга ВК**
# старался использовать максимально "стоковые" библиотеки пайтона, но запросы мне больше нравится отправлять библиотекой requests
# *бота надо зарегать у https://t.me/BotFather (более подробная инфа гуглится по "создать бота в телеграм") и добавить в свой канал, сделав админом
# **при желании можно запускать по расписанию/интервалу для авторепостов (cron, apscheduler и другие варианты)
# лично я запускал скрипт в venv'е другого проекта, где уже была установлена библиотека requests
# если будете использовать - упомяните меня или сообщите мне об этом, пожалуйста, мне будет приятно знать, что это кому-то пригодилось
import requests # https://requests.readthedocs.io/en/latest/
import json
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s @ %(name)s: %(message)s',
                    datefmt='%d.%m.%Y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

vk_token = "vk_sukaVeryLooooOOooOoOong.toKEn" #получить токен: https://vkhost.github.io/
vk_domain = "imya_gruppy_ili_polzovatelya" #короткий адрес пользователя или сообщества
vk_offset = 1 #если есть закреплённый пост и его надо пропустить (иначе заменить на 0); количество пропускаемых постов в принципе
link = "https://api.vk.com/method/wall.get?domain=" + vk_domain + "&offset=" + str(vk_offset) + "&count=1&extended=0&access_token=" + vk_token + "&v=5.131"

tg_token = "1111:6yk-Bbl" #получить у https://t.me/BotFather. более подробная инфа гуглится по "создать бота в телеграм"
tg_chat = 0 #в какой чат (канал - это тоже чат) репостить; целочисленное значение


def получение_ссылки_на_хайрез(lst): #сюда скармливается кусок json'а, которым отвечает ВК, конкретно вложения поста
    urls = []
    for elem in lst: #перебор всех ключей в скормленном списке (да, оно определяется как список)
        if elem.get("type") == "photo": #если вложение имеет тип данных == фото, то
            photo = elem.get("photo", {}) #пиздим с вложения инфу по ключу "фото"
            sizes = photo.get("sizes", []) #из спижженного выковыриваем размеры пикч по ключу "sizes"
            for size in sizes: #среди всех размеров ищем самый большой
                if size.get("type") == "w": #который обозначается типом дубль-вэ
                    urls.append(size.get("url")) #берём ссылку на жепег
    if len(urls) == 1: return urls[0] #если только одна хайрез-картинка, то возвращаем строку
    elif len(urls) > 1: return urls #если больше, то возвращается список ссылок
    else: return None #если нихуя не найдено, то выдаст "None"


def main():
    r = requests.post(link) #просим у ВК данные по стене
    j = r.json() #машине надо знать, что это json
    upl = получение_ссылки_на_хайрез(j["response"]["items"][0]["attachments"]) #ссылко
    vk_post_link = "https://vk.com/wall" + str(j["response"]["items"][0]["from_id"]) + "_" + str(j["response"]["items"][0]["id"]) #строка с ссылкой на пост ВК в конце сообщения в телеге
    tgtxt_full = j["response"]["items"][0]["text"] + "\n\n" + vk_post_link #берём текст с ВК и присираем ссылку на пост ВК
    if len(tgtxt_full) > 1024: #подписи к фото, которые длиннее 1024 символов, нельзя (RTFM)
        tgtxt = vk_post_link #меняем текст подписи на ссылку на пост ВК
        doublepost = True #для разбиения на отдельные посты с текстом и картинкой
    else: tgtxt = tgtxt_full
    tg_method = "sendPhoto" #базово считаем, что репостим одну фотку
    if upl is None: #если ссылки на фото в хайрезе нет
        tg_method = "sendMessage" #значит, скорее всего, это сообщение с текстом, а не рисогенарт
    else: 
        if isinstance(upl, list): 
            tg_method = "sendMediaGroup" #если там не одна ссылка, а пачка, то надо использовать другой метод для телеги
            arr = [] #нужон массив
            for i, item in enumerate(upl): #перебираем массив
                media_item = {"type": "photo", "media": item} #вкидываем данные в его элементы
                if i == 0: media_item["caption"] = tgtxt #к первому элементу добавляем описание
                arr.append(media_item) #собираем 
            ja = json.dumps(arr) #делаем массив json-serialized (RTFM)
            payload = {"chat_id": tg_chat, "media": ja}
        else: payload = {"chat_id": tg_chat, "photo": upl, "caption": tgtxt} #параметры для формирования ссылки в телегу
    tg_push_link = "https://api.telegram.org/bot" + tg_token + "/" + tg_method #куда долбицца для отправки в телегу
    if tg_method == "sendMessage": 
        payload = {"chat_id": tg_chat, "text": tgtxt_full} #параметры для формирования ссылки
    if doublepost and tg_method != "sendMessage": #если надо даблпостить из-за ограничения на длину подписи к фото
        first_post_link = "https://api.telegram.org/bot" + tg_token + "/sendMessage" #формируем ссылку
        first_post_payload = {"chat_id": tg_chat, "text": tgtxt_full} #формируем параметры
        first = requests.post(first_post_link, params=first_post_payload) #отправляем в тг
        print(first.json()) #выводим ответ в консоль
    go = requests.post(tg_push_link, params=payload) #собсна отправка поста
    print(go.json()) #выводим ответ в консоль


if __name__ == '__main__':
    main()