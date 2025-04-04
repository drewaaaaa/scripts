#!/usr/bin/bash
# скрипт для постинга охуенных советов в тг-канал (через тг-бота)
advice_url="https://fucking-great-advice.ru/api/random"
response=$(curl -s "$advice_url")
text=$(echo "$response"|jq -r '.text')
# это адское регулярное выражение писал я, зарывшись в мануал, ибо чатгпт предлагал ересь, но зато он вполне себе мог объяснить мой вариант
# я просто считаю, что слово "блять" не существует, а междометие "блядь" должно обособляться \G.
cleaned_text=$(perl -pe '
s/блять/блядь/g;
s/(?<=\S) бля /, бля, /g;
s/(?<=\S) блядь,/, блядь, /g;
s/(?<=\S) блядь!/, блядь!/g;
s/(?<=\S) блядь (?=\S)/, блядь, /g;
s/, —/ —/g;
s/,,/,/g;
s/\s\s/ /g;
' <<< "$text")
# разделение на строки по 25 символов, чтобы было красиво
imgtxt=$(echo "$cleaned_text"|fold -s -w 25)
num=$(((RANDOM%78)+1))
# у них там 78 пикч лежит
advice_img_url="https://fucking-great-advice.ru/data/frontpage/${num}.jpg"
wget -q -O advice.jpg "$advice_img_url"
# нанесение надписи по центру картинки шрифтом БЕБАС с обводкой
convert "advice.jpg" -gravity center -fill white -stroke black -strokewidth 1 -font BebasNeueBold -pointsize 123 -annotate +0+0 "$imgtxt" "advice.jpg"
# тут нужен токен бота перед методом
curl -s -X POST "https://api.telegram.org/bot70k:e-N/sendPhoto" \
	-F "chat_id=numbers or @channelname" \
	-F "caption=#советдня" \
	-F "photo=@advice.jpg"
 # да-да, для использования скрипта нужен тг-бот, который может постить в чате/канале, установленный шрифт бебас (или любой другой на ваш вкус), установленный imagemagick, остальное вроде обычное есть типа wget, curl и perl.
