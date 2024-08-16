#!/usr/bin/bash
#скрипт для обновления тг-поста с проигрываемым треком через скробблинг с ласты (через тг-бота)
# Переменные для URL-ов
LASTFM_URL="https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=USERNAME&api_key=APIKEYAPIKEYAPIKEY&format=json&nowplaying=true&limit=1"
TELEGRAM_URL="https://api.telegram.org/bot70:kE-N/editMessageMedia"

# URL и подписи для пустого состояния
AAempty="https://lastfm.freetls.fastly.net/i/u/300x300/4128a6eb29f94943c9d206c08e625904.jpg"
#↑можно другое изображение, ссылка же
captionEmpty="Сейчас ничего не воспроизводится 
#nowplaying"
chat_id="@tvoykanalilichat"
message_id="88"

# Выполняем запрос на Last.fm
response=$(curl -s "$LASTFM_URL")

# Проверяем наличие ключа "@attr", который указывает на воспроизведение трека
now_playing=$(echo "$response" | jq -r '.recenttracks.track[0]."@attr".nowplaying // empty')

if [[ -z "$now_playing" ]]; then
    # Если ключа нет, значит сейчас ничего не воспроизводится
    media=$(jq -n --arg type "photo" --arg media "$AAempty" --arg caption "$captionEmpty" \
                 '{type: $type, media: $media, caption: $caption, parse_mode: "HTML"}')
else
    # Если ключ есть, извлекаем нужные данные
    artist=$(echo "$response" | jq -r '.recenttracks.track[0].artist."#text"')
    track=$(echo "$response" | jq -r '.recenttracks.track[0].name')
    AAmusic=$(echo "$response" | jq -r '.recenttracks.track[0].image[3]."#text"')

    # Формируем caption для текущего трека
    captionMusic="${artist} — ${track} 
#nowplaying"

    # Формируем JSON для отправки в Telegram
    media=$(jq -n --arg type "photo" --arg media "$AAmusic" --arg caption "$captionMusic" \
                 '{type: $type, media: $media, caption: $caption, parse_mode: "HTML"}')
fi

# Формируем тело POST-запроса
post_data=$(jq -n --arg chat_id "$chat_id" --arg message_id "$message_id" --argjson media "$media" \
                '{chat_id: $chat_id, message_id: $message_id, media: $media}')

# Отправляем данные в Telegram
curl -s -X POST "$TELEGRAM_URL" -H "Content-Type: application/json" -d "$post_data"
