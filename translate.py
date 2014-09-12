#!/usr/bin/env python
"""
Неофициальный клиент для translate.yandex.ru

Документация к API: 
http://api.yandex.ru/translate/doc/dg/concepts/About.xml
"""
import os
import urllib.parse
import urllib.request
import json


# Переменная окружения, указывающая на файл с ключем
KEY_ENVIRON_VARIABLE = "YANDEX_TRANSLATOR_KEY"

# URL переводчика
URL = "https://translate.yandex.net/api/v1.5/tr.json/"

PLAIN = 'plain'
HTML = 'html'

OK = 200


class APIException(Exception):
    """
    Базовый класс исключения для ошибок API
    """
    message = None   # cообщение, передоваемое в исключение

    def __init__(self):
        assert self.message is not None
        super(APIException, self).__init__(self.message)


class BadKeyError(APIException):
    message = "Неправильные ключ API"


class KeyBlockedError(APIException):
    message = "Ключ API заблокирован"


class TriesLimitError(APIException):
    message = "Превышено суточное ограничение на количество запросов"


class TextLimitError(APIException):
    message = "Превышено суточное ограничение на объем переведенного текста"


class TextLengthLimitError(APIException):
    message = "Превышен максимально допустимый размер текста"


class CantTranslateError(APIException):
    message = "Текст не может быть переведен"


class NotSupportedError(APIException):
    message = "Заданное направление перевода не поддерживается"


# отображение кодов ошибок на исколючения
exception_map = {
    401: BadKeyError,
    402: KeyBlockedError,
    403: TriesLimitError,
    404: TextLimitError,
    413: TextLengthLimitError,
    422: CantTranslateError,
    501: NotSupportedError
}


def throw(code):
    """
    Возбуждает исключение, соответствующее коду ошибки

    :param int code: Код ошибки
    """
    assert code in exception_map
    raise exception_map[code]


class YTranslator(object):
    def __init__(self, key_path=None, api_key=None):
        self.__API_KEY = None
        if api_key:
            self.init_key(api_key)
        else:
            self.init_key_from_path(key_path)
    
    def detect(self, *, text):
        """
        Определение языка, на котором написан заданный текст.

        :param str text: Текст для определения языка
        :return: код языка, на котором написан текст
        """
        response = self.__call_api("detect", text=text)
        return response["lang"]

    def __call_api(self, method, **kwargs):
        """
        Вызов метода ``method``
    
        :param str method: Название метода API
        :return: JSON ответ
        """
        assert self.__API_KEY, "Не считан ключ API"

        kwargs['key'] = self.__API_KEY
        response = urllib.request.urlopen(
            urllib.parse.urljoin(URL, method),
            data=urllib.parse.urlencode(kwargs).encode("utf-8"))

        response = json.loads(response.read().decode("utf-8"))
        if response.get("code", OK) != OK:
            throw(response["code"])
        return response


    def translate(self, *, text, lang, format=PLAIN):
        """
        Перевод текста на заданный язык. 

        :param str text: Текст, который необходимо перевести
        :param str lang: Направление перевода.
            Может задаваться одним из следующих способов:
            * В виде пары кодов языков («с какого»-«на какой»), разделенных дефисом.
            Например, en-ru обозначает перевод с английского на русский.
            *В виде кода конечного языка (например ru).
            В этом случае сервис пытается определить исходный язык автоматически.
        :param str format: Формат текста.
            Возможны два значения:
            * plain — текст без разметки (значение по умолчанию);
            * html — текст в формате HTML.
        :return: перевод текста
        """
        response = self.__call_api("translate", text=text, lang=lang, format=format)
        return response["text"][0]

    def get_langs(self, *, ui=None):
        """
        Получение списка направлений перевода, поддерживаемых сервисом.

        :param str ui: Если задан, ответ будет дополнен расшифровкой кодов языков.
        Названия языков будут выведены на языке, код которого соответствует этому параметру.
        :return: список направлений перевода
        """
        params = dict()
        if ui is not None:
            params['ui'] = ui
        response = self.__call_api('getLangs', **params)
        return response["dirs"]

    def __get_environ_key_path(self):
        assert KEY_ENVIRON_VARIABLE in os.environ, (
            "Не установлена переменная окружения "
            "{}".format(KEY_ENVIRON_VARIABLE))

        path_to_key = os.environ[KEY_ENVIRON_VARIABLE]

        if not os.path.isfile(path_to_key):
            raise Exception(
                "{} должен быть допустимым обычным файлом!".format(path_to_key))
        
        elif not os.access(path_to_key, os.R_OK):
            raise Exception("Нет доступа к файлу {}!".format(path_to_key))

        return path_to_key

    def init_key(self, API_KEY):
        self.__API_KEY = API_KEY

    def init_key_from_path(self, path_to_key):
        self.init_key(self.__read_key(path_to_key))

    def __read_key(self, path_to_key=None):
        """
        Считывает ключ из файла, на который указывает ``KEY_ENVIRON_VARIABLE``
        """
        if not path_to_key: 
            path_to_key = self.__get_environ_key_path()

        with open(path_to_key, "rt") as f:
            for line in f.readlines():
                key, *value = line.strip().replace(" ", "").split("=")
                if key.lower() == "key":
                    break
            else:
                raise Exception("Ключ не найден!")

        if len(value) != 1:
            raise BadKeyError
        return value[0]  

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Yandex переводчик")
    parser.add_argument("--lang", dest='lang', default='none', help='Направление перевода')
    parser.add_argument("text", metavar='text', help='Текст, который необходимо перевести')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    lang, text = args.lang, args.text
    if lang == "none":
        text_lang = detect(text=text[:100])
        if text_lang != "ru":
            lang = "ru"
        else:
            lang = "en"

    ytrans = YTranslator()

    print("Language detected:\033[92m %s\033[00m"%(ytrans.detect(text=text)))
    print("Translated: \033[93m%s\033[00m"%(ytrans.translate(lang=lang, text=text)))
