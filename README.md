# ii-db-utils

ii-db-utils - это простейшие скрипты на python3 и bash для работы с классической текстовой базой данных ii и IDEC.
В `ii_functions.py` есть переменные `indexdir` и `msgdir`, где указывается альтернативный путь к индексу и сообщениям. По умолчанию идёт работа с базой в текущем каталоге.
Документация сетей IDEC и ii [здесь](http://ii-net.tk/idec-doc).

## emailtoii.py

С этим скриптом можно использовать ii-клиент для чтения входящих email-писем. Подход у него очень простой, html преобразуется в plaintext.
Для использования требуется установить fetchmail, procmail и html2text (python-версию). Примерные образцы конфигов здесь есть.

## sender.py

Эта вещь позволяет отправлять сообщения на удалённую станцию (как поинт). Полезно для роботов-автопостеров или собственных утилит. Формат файлов - обычный [msgline](http://ii-net.tk/idec-doc/?p=standarts) (без base64).

## ii-search.py

Утилита для поиска сообщений в базе.
* Ищет по эхам, отправителям, получателям, адресам станции, по временным промежуткам, по сабжу и тексту сообщения
* Если надо искать по всем значениям параметра поиска, то просто жмёте Enter
* По первым 4 параметрам поиска можно вводить несколько значений через разделитель (пробел или || для адреса и поинтов)
* Найденные сообщения сортируются по времени
* Если передать строку в качестве аргумента командной строки, то запишет в этот файл результаты в виде msgid

## ii-stats.py

Простейшая статистика: по эхам, сообщениям, поинтам и.т.д.

## ii-echocat.sh

Всего лишь выводит по N последних сообщений с каждой выбранной эхи с сортировкой по времени. Можно применять для conky или чего-нибудь подобного.

## view.py

Позволяет быстро просматривать сообщения в нужной эхоконференции.

Посмотреть все сообщения: `view.py echoarea.15`
Вывести последние пять: `view.py echoarea.15 -5:`
Первое сообщение: `view.py echoarea.15 0` (отсчёт идёт с нуля)
Со второго по четвёртое: `view.py echoarea.15 1:5`
Узнать количество сообщений в эхе: `view.py echoarea.15 len`

## checker.py и builder.py

`checker.py` проверяет базу данных на элементарные ошибки (дубли, пустые сообщения и несоответствие базы индексу). `builder.py` эти ошибки исправляет.

## delete-echoareas.py

Удаляет заданные эхоконференции вместе с сообщениями из базы данных. Ключи командной строки: *-q* для "молчаливого" режима, *-i* запрашивает подтверждение.

## offline-fetch.py

Оффлайн аналог *webfetch.py*. Синхронизирует базу данных между каталогами источника и назначения (эхоконференции задаются с клавиатуры). Может также не синхронизировать каталоги напрямую, а лишь генерировать бандл при указании необязательного параметра (см. далее).
Использование:

```
offline-fetch.py <БД-источник> <БД-назначение> [файл бандла]
```

## ii-bundle.py и ii-debundle.py

Упаковка и распаковка [бандлов](http://ii-net.tk/idec-doc/?p=standarts). Можно записывать туда содержимое как одной, так и сразу нескольких эхоконференций. Расположение базы данных в *ii-debundle.py* указывается через параметры.
Использование:

```
./ii-bundle.py <имя output-файла>
./ii-debundle.py <файл-бандл> <путь к директории БД>
```

## archive.py

Скрипт принимает в качестве аргументов название эхоконференции и дату в формате YYYY.MM.DD, затем создаёт файл-бандл с сообщениями из указанной эхи, отправленными до указанной даты.

Пример:

```
archive.py ii.14 2015.01.01
```

## sqlite-import.py и sqlite-export.py

Аналоги двух предыдущих утилит, только в качестве бандла используется база данных sqlite3.

```
./sqlite-export.py <имя output-файла>
./sqlite-import.py <файл-БД>
```

## xfileget.py

Скачивание файлов ноды через новое расширение `/x/file`. Требуется указать станцию и строку авторизации (в коде).

## ii-bb.sh

ii-клиент на чистом busybox.

Работает на busybox ash (стандартный шелл), который совместим с dash. Дополнительные необходимые апплеты: wget, vi, cat, mv, stat, dd, base64, head, tail, date, mkdir (вроде все).

В самом начале файла удобно расположены настройки.

Фетч идёт через старый добрый `/m`. Отправка через GET, потому что busybox-овский wget не поддерживает POST

###### Просмотр эх
```
# вся эха
ii-bb.sh view ii.test.14

# узнать количество сообщений
ii-bb.sh view ii.test.14 len

# конкретное сообщение (отсчёт с нуля)
ii-bb.sh view ii.test.14 9
```

###### Написание сообщений
```
# всем
ii-bb.sh write ii.14

# ответить на конкретное
ii-bb.sh write ii.14 1522
```

###### Фетч и отправка
```
ii-bb.sh send
ii.bb.sh fetch
```