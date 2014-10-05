yandex-translator
=================

Unoficial client to **[Yandex translator API](http://translate.yandex.ru/)

Installation
------------
python setup.py install

Settings
---------
To use this package you need Yandex translation API key.

You can get is here:
 http://api.yandex.ru/key/form.xml?service=trnsl

You have to create file with key like:

``key=the key you got``

and set environment variable YANDEX_TRANSLATOR_KEY, that contains path to this file.

Usage
-----
Package provides cli tool and interactive translator.

*Cli tool usage:
    ytranslate.py -h

*Interactive translator:
    ytrans-interactive.py
