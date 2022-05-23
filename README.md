# Skull Of Wisdom
Примитивная text-to-speech игрушка на основе Raspberry Pi, использующая экодинги лиц.
<p float="left">
 <img src="https://user-images.githubusercontent.com/70561974/168880886-5978e5cb-1007-4ceb-a523-d9ca04b95042.png" width="400"/>
<img src="https://user-images.githubusercontent.com/70561974/168880908-c9c0a72a-1d3d-41d0-a715-57d472213c42.png" width="400"/>
</p>

## Функционал
Мониторит видеопоток, при нахождении лица на фотографии считает энкодинг. Если экодинг нашелся среди известных, зачитывает случайное приветствие по имени. Если не нашелся - зачитывает случайное приветствие для неопознанного человека.

После произносит случайно выбранную дегенератскую фразу. Далее возвращается к мониторингу видеопотока. Среди списка фраз есть одна, присуждающая опознанному лицу приз. После того, как она была произнесена, она больше не повторяется. Эта ерунда была придумана для попойки на мой др, чтобы разбавить алкогольное отравление случайным набором мемов не первой свежести.

Приветствия, фразы, обращение к неопознанному человеку и прочие настройки лежат в конфиге.

## Сетап
1. Устаревший Raspberry Pi 3B+ 1Gb Ram 64Gb microSDHC,
2. Пожилая Genius Eye 320 SE 640x480,
3. Безымянная китайская портативная колонка S28 с антресоли,
4. Гипсовая голова синяя.

 ## Зависимости
 1. imutils и opencv-python для обработки изображений,
 2. festival для синтеза речи на unix, pyttsx3 для синтеза речи на windows,
 3. face-recognition для генерации энкодингов.

## Некоторая история создания
Изначально в качестве tts библиотеки использовался pyttsx3. Код писался на windows под пиво за пару вечеров после работы, так что качество кода соответствующее. На windows pyttsx3 вызывает библиотеку sapi5, которая имеет небольшой набор голосов, но прекрасное качество звучания, 10/10, господи, 10/10. 

На unix системах он вызывает espeak, качество звучания которого оцениваю как кал/10 даже после установки дополнительного русского словаря. Решил использовать festival, который работал лучше, но все равно на троечку - хуевые интонации, нет возможности выставить ударения в словах. Попвтки перейти на rhvoice не увенчались успехом, потмоу что под raspbian он билдиться так и не захотел. Итоговый результат был настолько херовым, что решил просто поставить за черепом виндовый ноутбук с вебкой. Обидно пиздец, кучу времени убил на сношения с raspbian.

Также выяснилось, что при подключении к колонке по bluetoth проглатывается начало воспроизводимых фраз, так как без поступления сигнала колонка спит и включается далеко не мгновенно. Благо и у колонки, и у ебучего коробка с микросхемами есть aux.

Поскольку есть желание добиться от raspberry хоть чего-то рабочего осталось, наверное, в будущем сооружу на его базе что-то англоговорящее, так как качество английского у festival еще более-менее.
